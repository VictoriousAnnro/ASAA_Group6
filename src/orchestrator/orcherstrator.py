import json
import time
import threading
import random
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


class RunState(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    ABORTED = auto()
    FAULTED = auto()


class StepState(Enum):
    PENDING = auto()
    RUNNING = auto()
    SUCCESS = auto()
    FAILED = auto()
    ABORTED = auto()


# ---------------------------
#  Safety Module
# ---------------------------

class SafetyModule:
    """
    Simulates safety flags like human presence and emergency stop.
    Orchestrator should check these frequently and abort quickly if set.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.human_present = False
        self.e_stop = False

    def set_human_present(self, present: bool):
        with self._lock:
            self.human_present = present
        print(f"[SAFETY] human_present set to {present}")

    def trigger_e_stop(self):
        with self._lock:
            self.e_stop = True
        print("[SAFETY] EMERGENCY STOP TRIGGERED")

    def clear_e_stop(self):
        with self._lock:
            self.e_stop = False
        print("[SAFETY] e_stop cleared")

    def is_safe(self) -> bool:
        with self._lock:
            return not self.human_present and not self.e_stop


# ---------------------------
#  Monitoring & Logging
# ---------------------------

class MonitoringLogger:
    def __init__(self):
        self.events = []

    def log(self, run_id: str, message: str, extra: Optional[Dict[str, Any]] = None):
        ts = time.time()
        entry = {"ts": ts, "run_id": run_id, "message": message}
        if extra:
            entry.update(extra)
        self.events.append(entry)
        # For now just print; later you can push this to DB, Kafka, etc.
        print(f"[{ts:.3f}][RUN:{run_id}] {message} | {extra or ''}")


# ---------------------------
#  Station simulator
# ---------------------------

class StationStatus(Enum):
    IDLE = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    ABORTED = auto()


class StationSimulator:
    """
    Simulates a robot station. Work is done on a worker thread so we can abort / check safety.
    """

    def __init__(self, name: str, avg_duration: float = 3.0, failure_rate: float = 0.1):
        self.name = name
        self.avg_duration = avg_duration
        self.failure_rate = failure_rate
        self._status = StationStatus.IDLE
        self._thread: Optional[threading.Thread] = None
        self._abort_flag = False
        self._lock = threading.Lock()

    def start(self, task_id: str, params: Dict[str, Any], safety: SafetyModule):
        with self._lock:
            if self._status == StationStatus.RUNNING:
                raise RuntimeError(f"{self.name} already running")
            self._status = StationStatus.RUNNING
            self._abort_flag = False

        def worker():
            print(f"[{self.name}] Starting task {task_id} with params {params}")
            # Simulate variable duration
            duration = random.uniform(self.avg_duration * 0.5, self.avg_duration * 1.5)
            start = time.time()
            try:
                while time.time() - start < duration:
                    # Check abort flag
                    if self._abort_flag:
                        with self._lock:
                            self._status = StationStatus.ABORTED
                        print(f"[{self.name}] Task {task_id} aborted")
                        return

                    # Check safety
                    if not safety.is_safe():
                        with self._lock:
                            self._status = StationStatus.ABORTED
                        print(f"[{self.name}] Task {task_id} aborted due to safety")
                        return

                    time.sleep(0.1)

                # Random failure
                if random.random() < self.failure_rate:
                    with self._lock:
                        self._status = StationStatus.FAILED
                    print(f"[{self.name}] Task {task_id} failed")
                else:
                    with self._lock:
                        self._status = StationStatus.COMPLETED
                    print(f"[{self.name}] Task {task_id} completed")
            except Exception as e:
                with self._lock:
                    self._status = StationStatus.FAILED
                print(f"[{self.name}] Exception: {e}")

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()

    def status(self) -> StationStatus:
        with self._lock:
            return self._status

    def abort(self):
        with self._lock:
            self._abort_flag = True

    def wait_until_finished(self, timeout: Optional[float] = None):
        if self._thread:
            self._thread.join(timeout=timeout)


# ---------------------------
#  Data classes
# ---------------------------

@dataclass
class RecipeStep:
    id: int
    station: str
    params: Dict[str, Any]
    state: StepState = StepState.PENDING
    started_at: Optional[float] = None
    finished_at: Optional[float] = None


@dataclass
class ProductionRun:
    run_id: str
    order_id: str
    steps: List[RecipeStep]
    state: RunState = RunState.PENDING
    current_step_index: int = 0


# ---------------------------
#  Orchestration Core
# ---------------------------

class OrchestratorCore:
    """
    State machine that executes a ProductionRun step by step,
    talks to station simulators, checks safety, and logs everything.
    """

    def __init__(self, stations: Dict[str, StationSimulator],
                 safety: SafetyModule,
                 logger: MonitoringLogger):
        self.stations = stations
        self.safety = safety
        self.logger = logger

    def execute_run(self, run: ProductionRun):
        self.logger.log(run.run_id, "Run starting", {"order_id": run.order_id})
        run.state = RunState.IN_PROGRESS

        try:
            while run.current_step_index < len(run.steps):
                if not self.safety.is_safe():
                    self._abort_all_stations(run, reason="Safety condition triggered")
                    run.state = RunState.ABORTED
                    self.logger.log(run.run_id, "Run aborted due to safety")
                    return

                step = run.steps[run.current_step_index]
                self._execute_step(run, step)

                if step.state == StepState.SUCCESS:
                    run.current_step_index += 1
                    continue
                elif step.state in (StepState.ABORTED, StepState.FAILED):
                    # simple strategy: abort whole run
                    run.state = RunState.ABORTED if step.state == StepState.ABORTED else RunState.FAULTED
                    self.logger.log(run.run_id, "Run ended early", {"run_state": run.state.name})
                    return

            run.state = RunState.COMPLETED
            self.logger.log(run.run_id, "Run completed successfully")

        except Exception as e:
            run.state = RunState.FAULTED
            self.logger.log(run.run_id, "Run faulted with exception", {"error": str(e)})

    def _execute_step(self, run: ProductionRun, step: RecipeStep):
        step.state = StepState.RUNNING
        step.started_at = time.time()

        station_name = step.station.lower()
        station = self.stations.get(station_name)
        if not station:
            self.logger.log(run.run_id, "Unknown station", {"station": station_name})
            step.state = StepState.FAILED
            return

        task_id = f"{run.run_id}-STEP-{step.id}"
        self.logger.log(run.run_id, f"Starting step {step.id} on {station_name}", {"params": step.params})

        station.start(task_id, step.params, self.safety)

        # Wait for station to finish, checking safety and allowing timeout
        start_wait = time.time()
        timeout = 30.0  # per-step timeout, can be tuned

        while True:
            status = station.status()

            if status in (StationStatus.COMPLETED, StationStatus.FAILED, StationStatus.ABORTED):
                break

            if time.time() - start_wait > timeout:
                self.logger.log(run.run_id, "Step timeout, aborting station",
                                {"step_id": step.id, "station": station_name})
                station.abort()
                status = StationStatus.ABORTED
                break

            if not self.safety.is_safe():
                self.logger.log(run.run_id, "Safety triggered during step, aborting",
                                {"step_id": step.id, "station": station_name})
                station.abort()
                status = StationStatus.ABORTED
                break

            time.sleep(0.1)

        step.finished_at = time.time()

        if status == StationStatus.COMPLETED:
            step.state = StepState.SUCCESS
            self.logger.log(run.run_id, f"Step {step.id} completed", {"duration": step.finished_at - step.started_at})
        elif status == StationStatus.FAILED:
            step.state = StepState.FAILED
            self.logger.log(run.run_id, f"Step {step.id} failed", {})
        elif status == StationStatus.ABORTED:
            step.state = StepState.ABORTED
            self.logger.log(run.run_id, f"Step {step.id} aborted", {})

    def _abort_all_stations(self, run: ProductionRun, reason: str):
        self.logger.log(run.run_id, "Aborting all stations", {"reason": reason})
        for name, station in self.stations.items():
            station.abort()


# ---------------------------
#  Example "main" for local testing
# ---------------------------

def load_example_recipe() -> ProductionRun:
    # In reality this would come from MongoDB or Scheduler via Kafka
    recipe_json = {
        "run_id": "RUN-000",
        "order_id": "ORDER-001",
        "steps": [
            {"id": 1, "station": "chassis",  "params": {"model": "Sedan"}},
            {"id": 2, "station": "engine",   "params": {"engine": "V8"}},
            {"id": 3, "station": "wheels",   "params": {}},
            {"id": 4, "station": "interior", "params": {"interior": "Sport"}},
            {"id": 5, "station": "paint",    "params": {"color": "Red"}},
            {"id": 6, "station": "lights",   "params": {}}
        ]
    }

    steps = [RecipeStep(**step) for step in recipe_json["steps"]]
    return ProductionRun(run_id=recipe_json["run_id"],
                         order_id=recipe_json["order_id"],
                         steps=steps)


def main():
    safety = SafetyModule()
    logger = MonitoringLogger()

    # Create one simulator per station type
    stations = {
        "chassis": StationSimulator("ChassisRobot", avg_duration=2.0),
        "engine": StationSimulator("EngineRobot", avg_duration=3.0),
        "wheels": StationSimulator("WheelsRobot", avg_duration=1.5),
        "interior": StationSimulator("InteriorRobot", avg_duration=2.5),
        "paint": StationSimulator("PaintRobot", avg_duration=4.0),
        "lights": StationSimulator("LightsRobot", avg_duration=1.5),
    }

    orchestrator = OrchestratorCore(stations=stations, safety=safety, logger=logger)
    production_run = load_example_recipe()

    # OPTIONAL: simulate a safety event after some time in a background thread
    def simulate_safety():
        time.sleep(6)
        safety.set_human_present(True)  # or safety.trigger_e_stop()

    threading.Thread(target=simulate_safety, daemon=True).start()

    orchestrator.execute_run(production_run)
    print(f"Final run state: {production_run.state}")
    for step in production_run.steps:
        print(f"Step {step.id} -> {step.state.name}, duration={ (step.finished_at or 0) - (step.started_at or 0):.2f}s")


if __name__ == "__main__":
    main()
