# Intro

Search Azure quantum tutorial to arrive at [this documentation](https://docs.microsoft.com/en-us/azure/quantum/).

Get started:
* [Create an Azure Quantum workspace](https://docs.microsoft.com/en-us/azure/quantum/how-to-create-workspace?tabs=tabid-quick)
    * Create a resource; select Azure Quantum, follow the steps > end result is a quantum workspace Resource Group
    * Next steps and content links:
        * [Jupyter](https://docs.microsoft.com/en-us/azure/quantum/get-started-jupyter-notebook)
        * [Random number generator](https://docs.microsoft.com/en-us/azure/quantum/quickstart-microsoft-qc)
        * [Optimization problem solver](https://docs.microsoft.com/en-us/azure/quantum/quickstart-microsoft-qio)
        * [Submit a circuit to Azure Quantum](https://docs.microsoft.com/en-us/azure/quantum/quickstart-microsoft-qiskit)
        * [Quantum job pricing](https://docs.microsoft.com/azure/quantum/azure-quantum-job-costs) (not terribly illuminating in March 2022)
        * [Cirq circuits: Submitting to Azure Quantum documentation](https://docs.microsoft.com/azure/quantum/quickstart-microsoft-cirq?pivots=platform-ionq)
    * The **quantum workspace** is hosted in the Resource Group. Select it to enter that environment.
    * Add some tags to provide context for the casual or future observer
    * Left menu: Select **Notebooks**
    * Seven samples are available: Three variations of Hello World and four additional
        * I copy all of them to the **`My Notebooks`** folder
    * I run "all cells" for the hello-world-cirq-ionq notebook: That takes a couple minutes
        * I'm informed that just cost me 1 USD
        * This appears to be a stylized, hosted Jupyter notebook server
        * The steps appear to be...
            * create a **`service`** connection to the quantum workspace
            * examine **`service.targets`** to find both honeywell and ionq targets
            * create a seven-line Python program starting with **`import cirq`**
            * submit this program as a job to the **`"ionq.simulator"`** target
            * await the results: 35 seconds for example; printout is probabilities for two states
            * use **`cirq.vis`** to plot state histogram
            * estimate the cost: 1 USD for the simulator
                * I replaced **`.simulator`** with **`.qpu`** and re-ran
                * This time 10 minutes elapsed: No response
                * Question: Can I close up shop and come back later to see what happened?
                * Question: Is the qpu approach appreciably more expensive that 1 USD?


Above was a first session. The **`qpu`** job would not complete; so I left. 
Session two: Re-open the quantum workspace: *Notebooks* in the left sidebar: My notebooks folder: Ok. 
There are seven notebooks copied here: grovers-search,
hello-world-cirq-ionq, hello-worlds for qiski and qsharp; plus hidden-shift, noisy-deutsch-jozsa, 
and finally parallel-qrng. 


The hello-world-cirq-ionq notebook has several runnable Python cells. The first one creates a **`service`** object 
(9 seconds). This (second cell) lists eight services including the **`ionq`** **`simulator`** and **`qpu`**. 
Last time I ran the simulator and then submitted the qpu job that did not finish. Unfortunately I can't
seem to run **`service.get_jobs()`** without the job id; which was printed but the output was erased; so I 
restarted it. This time the job id is `0711b826-af98-11ec-b345-00155d329a60`. 

Now that the **`job`** object is active: I can recover the job id with **`job.job_id()`**. 

Oh, but wait: There is a left menu item Job management: Table: jobs with ids and targets. Click the Name for 
Job details: Apparently the qpu job took 17 hours to run but only 2 seconds of execution time. From Job details:
Download input and output: 

```
{"qubits": 1, "circuit": [{"gate": "h", "targets": [0]}]}
```

and

```
{"histogram":{"0":0.47,"1":0.53}}
```

For 100 trials of a coin toss this is reasonable. 



