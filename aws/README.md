# Amazon Braket

Start by finding the Quantum Technologies. Agree to terms and start 'Enable Amazon Braket'.


Here are some notes; the elaboration is still needed but for what it is worth:
- Shots are circuit runs; tasks are some number of shots
- Pay for jobs by Device rate (click on the Device in the control console)
    - Task cost is $0.30
    - Shot cost is epsilon per (varies)
    - Exception: Simulators are priced per EC2 cost / minute
    - Notice Devices have associated Regions
        - Six quantum Devices
        - Three simulator Devices
- Direct access is via a Notebook server with examples written in Python
    - Start the notebook server; it has its own local simulator
    - Use Simulators running on EC2
    - Use quantum devices
- Control page left menu: Can look up jobs to see completion status, download results.

```
{
    "braketSchemaHeader": {
        "name": "braket.task_result.gate_model_task_result",
        "version": "1"
    },
    "measurements": [
        [
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1
        ],
...etcetera...
```
  
  
