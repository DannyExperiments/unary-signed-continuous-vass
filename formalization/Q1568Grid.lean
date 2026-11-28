import Std

namespace SignedGrid

/-- Allocate an integer mass to a positive bounded share for each occurrence.
This is the common-denominator allocation in the short-run reconstruction. -/
theorem shares (count cap mass : Nat) (positiveCap : 0 < cap)
    (lo : count ≤ mass) (hi : mass ≤ count * cap) :
    ∃ parts : List Nat, parts.length = count ∧ parts.sum = mass ∧
        ∀ x ∈ parts, 1 ≤ x ∧ x ≤ cap := by
  induction count generalizing mass with
  | zero =>
    have : mass = 0 := by simpa using hi
    subst mass
    exact ⟨[], by simp⟩
  | succ n ih =>
    let x := min cap (mass - n)
    have hc : mass ≤ n * cap + cap := by simpa [Nat.succ_mul] using hi
    have hx : 1 ≤ x ∧ x ≤ cap ∧ x ≤ mass := by dsimp [x]; omega
    have lower : n ≤ mass - x := by dsimp [x]; omega
    have capacity : n ≤ n * cap := by simpa using Nat.mul_le_mul_left n positiveCap
    have upper : mass - x ≤ n * cap := by dsimp [x]; omega
    obtain ⟨tail, len, sum, bounds⟩ := ih (mass-x) lower upper
    refine ⟨x :: tail, by simp [len], ?_, ?_⟩
    · simp only [List.sum_cons, sum]; omega
    · intro y hy
      rcases List.mem_cons.mp hy with rfl | h
      · exact ⟨hx.1, hx.2.1⟩
      · exact bounds y h
#print axioms shares
end SignedGrid
