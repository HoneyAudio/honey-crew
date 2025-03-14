# CrewAI CLI Documentation

The CrewAI CLI provides a set of commands to interact with CrewAI, allowing you to create, train, run, and manage crews and pipelines.

## Installation

To use the CrewAI CLI, make sure you have CrewAI & Poetry installed:

```shell
pip install crewai poetry
```

## Basic Usage

The basic structure of a CrewAI CLI command is:

```shell
crewai [COMMAND] [OPTIONS] [ARGUMENTS]
```

## Available Commands

### 1. Create

Create a new crew or pipeline.

```shell
crewai create [OPTIONS] TYPE NAME
```

- `TYPE`: Choose between "crew" or "pipeline"
- `NAME`: Name of the crew or pipeline
- `--router`: (Optional) Create a pipeline with router functionality

Example:

```shell
crewai create crew my_new_crew
crewai create pipeline my_new_pipeline --router
```

### 2. Version

Show the installed version of CrewAI.

```shell
crewai version [OPTIONS]
```

- `--tools`: (Optional) Show the installed version of CrewAI tools

Example:

```shell
crewai version
crewai version --tools
```

### 3. Train

Train the crew for a specified number of iterations.

```shell
crewai train [OPTIONS]
```

- `-n, --n_iterations INTEGER`: Number of iterations to train the crew (default: 5)
- `-f, --filename TEXT`: Path to a custom file for training (default: "trained_agents_data.pkl")

Example:

```shell
crewai train -n 10 -f my_training_data.pkl
```

### 4. Replay

Replay the crew execution from a specific task.

```shell
crewai replay [OPTIONS]
```

- `-t, --task_id TEXT`: Replay the crew from this task ID, including all subsequent tasks

Example:

```shell
crewai replay -t task_123456
```

### 5. Log-tasks-outputs

Retrieve your latest crew.kickoff() task outputs.

```shell
crewai log-tasks-outputs
```

### 6. Reset-memories

Reset the crew memories (long, short, entity, latest_crew_kickoff_outputs).

```shell
crewai reset-memories [OPTIONS]
```

- `-l, --long`: Reset LONG TERM memory
- `-s, --short`: Reset SHORT TERM memory
- `-e, --entities`: Reset ENTITIES memory
- `-k, --kickoff-outputs`: Reset LATEST KICKOFF TASK OUTPUTS
- `-a, --all`: Reset ALL memories

Example:

```shell
crewai reset-memories --long --short
crewai reset-memories --all
```

### 7. Test

Test the crew and evaluate the results.

```shell
crewai test [OPTIONS]
```

- `-n, --n_iterations INTEGER`: Number of iterations to test the crew (default: 3)
- `-m, --model TEXT`: LLM Model to run the tests on the Crew (default: "gpt-4o-mini")

Example:

```shell
crewai test -n 5 -m gpt-3.5-turbo
```

### 8. Run

Run the crew.

```shell
crewai run
```

<Note>
Make sure to run these commands from the directory where your CrewAI project is set up. 
Some commands may require additional configuration or setup within your project structure.
</Note>
