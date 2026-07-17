import subprocess

controllers = [
    ("Fixed", "run_fixed.py"),
    ("Adaptive", "run_adaptive.py"),
    ("Dynamic", "run_dynamic.py"),
    ("Q-learning", "run_qtest.py"),
    ("DQN", "run_dqn_test.py")
]

NUM_SEEDS = 10

for name, script in controllers:

    print(f"\n===== {name} =====")

    for seed in range(NUM_SEEDS):

        print(f"Seed {seed}")

        subprocess.run(
            [
                "python",
                script,
                str(seed)
            ],
            check=True
        )