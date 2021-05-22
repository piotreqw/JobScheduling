from JobSchedulingWithSlack import Workspace


def print_progress(i, max_i) -> None:
    spaces = " " * (max_i - i)
    print(f"\r[{'=' * i}{spaces}]{100 * i / max_i}%", flush=True, end="")


def test_sorting__simplified(max_iterations=500) -> None:
    """Function tests various sorting methods looking for the one with best simplified sorting results"""
    workspace = Workspace()

    utilisation_per_sorting = {}
    iteration = 0

    while iteration <= max_iterations:
        print_progress(iteration, max_iterations)
        iteration += 1
        for sorting_type in range(0, 384):
            workspace.sort_tasks(sorting_type)
            workspace.allocate_tasks__simplified()

            if sorting_type in utilisation_per_sorting.keys():
                utilisation_per_sorting[sorting_type] = (utilisation_per_sorting[sorting_type] * iteration
                                                         + workspace.workforce.workforce_utilization()) \
                                                        / (iteration + 1)
            else:
                utilisation_per_sorting[sorting_type] = workspace.workforce.workforce_utilization()

    sorted_dict = sorted(utilisation_per_sorting.items(), key=lambda x: x[1])

    for sorting_type, utilization in sorted_dict:
        print(
            f'Sorting type:{sorting_type} utilisation:{utilization:.2f} '
            f'sorting:{Workspace.ALL_SORTING[sorted_dict[sorting_type][0]]}', flush=True)


def test_simplified_vs_complete_allocation(max_iterations=20, total_tasks_time=450 // 15) -> None:
    """Function tests simplified allocation algorithm, comparing results to simplified_complete allocation
    Result equals to 90% means in 90% of cases tasks couldn't have been allocated to less employees"""
    workspace = Workspace()

    result = []
    for i in range(0, max_iterations):
        print_progress(i, max_iterations)

        workspace.generate_random_tasks(total_tasks_time)

        workspace.sort_tasks(workspace.best_sorting__simplified())
        workspace.allocate_tasks__simplified()

        result.append(workspace.allocate_tasks__complete(len(workspace.workforce.employees_list) - 1))

    print(f' Done', flush=True)
    print(f'Simplified efficiency ratio {100 * (max_iterations - sum(result)) / max_iterations:.1f}%', flush=True)

def test_simplified_vs_complete_simplified_allocation(max_iterations=20, total_tasks_time=600 // 15) -> None:
    """Function tests simplified allocation algorithm, comparing results to complete allocation
    Result equals to 90% means in 90% of cases tasks couldn't have been allocated to less employees"""
    workspace = Workspace()

    result = []
    for i in range(0, max_iterations):
        print_progress(i, max_iterations)

        workspace.generate_random_tasks(total_tasks_time)

        workspace.sort_tasks(workspace.best_sorting__simplified())
        workspace.allocate_tasks__simplified()

        workspace.check_slacks_for_min_employees(print_text=False)

        result.append(workspace.minimum_employees_no < (len(workspace.workforce.employees_list) - 1))

    print(f' Done', flush=True)
    print(f'Simplified efficiency ratio {100 * (max_iterations - sum(result)) / max_iterations:.1f}%', flush=True)

def test_slack_for_min_employees_simplified_complete_allocation(total_tasks_time=450 // 15) -> None:
    """Function tests simplified allocation with best slack combination
    Function allocates tasks to minimum possible number of employees"""
    workspace = Workspace()
    workspace.generate_random_tasks(total_tasks_time)
    print('Checking slacks')
    workspace.check_slacks_for_min_employees(print_text=False)
    print('Allocating tasks')
    workspace.allocate_tasks__simplified_with_defined_slack()
    workspace.list_tasks()
    workspace.workforce.list_employees()


def test_optimized_allocation(total_tasks_time = 300 // 15) -> None:
    """In development - function is looking if possible to minimize number of employees required by moving
    slack for overlapping tasks."""
    workspace = Workspace()
    workspace.generate_random_tasks(total_tasks_time)
    workspace.sort_tasks()
    workspace.workforce.list_employees()
    workspace.optimize_no_of_employees_simplified_allocation()


if __name__ == '__main__':
    test_simplified_vs_complete_simplified_allocation() #Efficiency ~95%
