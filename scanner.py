import random

def generate_signal():

    signals = ["BUY","SELL","WAIT"]

    confidence = random.randint(
        55,
        75
    )

    return {

        "signal": random.choice(signals),

        "confidence": confidence,

        "tp": round(
            random.uniform(
                20,
                100
            ),
            2
        ),

        "sl": round(
            random.uniform(
                10,
                50
            ),
            2
        )

    }
