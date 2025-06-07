from dataclasses import dataclass, field
from typing import List, Optional
from pathlib import Path
import heapq
from collections import defaultdict

@dataclass
class Task:
    id: int
    processing_time: int

@dataclass
class Machine:
    id: int
    current_load: int = 0
    max_task_time: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.current_load += task.processing_time
        self.max_task_time = max(self.max_task_time, self.current_load)

    def remove_task(self, task: Task):
        self.tasks.remove(task)
        self.current_load -= task.processing_time
        self.max_task_time = max([task.processing_time for task in self.tasks], default=0)

    def is_empty(self):
        return not self.tasks
    
class ParallelMachineScheduler:
    def __init__(self, tasks: List[Task], num_machines: int):
        self.tasks = sorted(tasks, key=lambda x: x.processing_time, reverse=True)
        self.machines = [Machine(id=i) for i in range(num_machines)]
        self.best_schedule: Optional[List[Machine]] = None
        self.best_makespan = float('inf')

    def _get_greedy_solution(self):
        machines = [Machine(id=i) for i in range(len(self.machines))]

        # 直接按照任务的处理时间从大到小分配给每个机器
        for i in range(min(len(self.tasks), len(self.machines))):
            machines[i].add_task(self.tasks[i])
        
        # 把剩余的任务分配给处理时间最短的机器
        for task in self.tasks[len(self.machines):]:
            machine = min(machines, key=lambda x: x.max_task_time)
            machine.add_task(task)

        return max([machine.current_load for machine in machines])
        
    def _is_valid_assignment(self, machine: Machine, prev_machine: Machine, task: Task) -> bool:
        if machine.is_empty():
            # 如果机器的最大任务时间小于当前任务的处理时间，则情况重复
            return prev_machine.max_task_time >= task.processing_time
        return True
    
    def _backtrack(self, task_idx: int, current_makespan: int) -> None:
        # 终止条件
        if task_idx == len(self.tasks):
            if current_makespan < self.best_makespan:
                self.best_makespan = current_makespan
                self.best_schedule = []
                for m in self.machines:
                    new_machine = Machine(m.id)
                    new_machine.current_load = m.current_load
                    new_machine.max_task_time = m.max_task_time
                    new_machine.tasks = m.tasks.copy()
                    self.best_schedule.append(new_machine)
            return
        
        current_task = self.tasks[task_idx]

        for machine in self.machines:
            new_makespan = max(current_makespan, machine.current_load + current_task.processing_time)

            if new_makespan >= self.best_makespan:
                continue

            if machine.is_empty() and machine.id > 0:
                if not self._is_valid_assignment(machine, self.machines[machine.id - 1], current_task):
                # 确保分配任务的时候按降序排列，避免重复
                    break

            # 选择当前任务
            machine.add_task(current_task)
            self._backtrack(task_idx + 1, new_makespan)
            machine.remove_task(current_task)

    def solve(self) -> tuple[float, List[Machine]]:
        self.best_makespan = self._get_greedy_solution()
        self._backtrack(0, 0)
        return self.best_schedule, self.best_makespan
    
    def print_solution(self) -> None:
        if not self.best_schedule:
            print("没找到最优解")
            return

        print("\n=== Optimal Schedule ===")
        print(f"最佳调度时间为: {self.best_makespan}")
        print("\n机器分配情况:")
        for machine in self.best_schedule:
            task_str = ", ".join(f"T{task.id}({task.processing_time})" 
                               for task in machine.tasks)
            print(f"Machine {machine.id}: [{task_str}] "
                  f"Load: {machine.current_load}")


for file in ['test1.txt', 'test2.txt', 'test3.txt']:
    print(f"\n=== {file} ===")
    with open(file, 'r') as f:
        n, num_machines = map(int, f.readline().split())
        processing_times = list(map(int, f.readline().split()))
        tasks = [Task(i, t) for i, t in enumerate(processing_times)]

    scheduler = ParallelMachineScheduler(tasks, num_machines)
    makespan, schedule = scheduler.solve()

    # 打印结果
    scheduler.print_solution()