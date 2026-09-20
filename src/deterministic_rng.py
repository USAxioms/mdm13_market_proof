class DeterministicRNG:
    """
    Integer-only deterministic generator.

    This is deliberately simple and not cryptographic.
    """

    MOD = 2**64
    A = 6364136223846793005
    C = 1442695040888963407

    def __init__(self, seed=42):
        self.state = seed % self.MOD

    def next_u64(self):
        self.state = (self.A * self.state + self.C) % self.MOD
        return self.state

    def signed(self, amplitude):
        n = self.next_u64()
        centered = n - 2**63
        return (centered * amplitude) // 2**63