(define (problem liquidsort_task)
  (:domain LiquidSort)
  (:objects
    b0 b1 b2 b3 b4 b5 b6 - beaker
    c0 c1 c2 c3 c4 - color
    l0 l1 l2 l3 l4 - level
  )

  (:init
    ; --- Geometry of the game (static) ---
    (is-bottom l0)
    (succ l0 l1)
    (succ l1 l2)
    (succ l2 l3)
    (succ l3 l4)

    ; --- Defining initial state of the beakers ---
    (has-color b0 l1 c0)
    (has-color b0 l2 c1)
    (has-color b0 l3 c2)
    (has-color b0 l4 c3)
    (top b0 l4)
    (has-color b1 l1 c1)
    (has-color b1 l2 c0)
    (has-color b1 l3 c4)
    (has-color b1 l4 c1)
    (top b1 l4)
    (has-color b2 l1 c0)
    (has-color b2 l2 c3)
    (has-color b2 l3 c0)
    (has-color b2 l4 c2)
    (top b2 l4)
    (has-color b3 l1 c4)
    (has-color b3 l2 c3)
    (has-color b3 l3 c1)
    (has-color b3 l4 c4)
    (top b3 l4)
    (has-color b4 l1 c2)
    (has-color b4 l2 c4)
    (has-color b4 l3 c3)
    (has-color b4 l4 c2)
    (top b4 l4)
    (top b5 l0)
    (top b6 l0)
  )

  (:goal (and
    ; Goal for color c0
    (or
      (and (has-color b0 l1 c0) (has-color b0 l2 c0) (has-color b0 l3 c0) (has-color b0 l4 c0))
      (and (has-color b1 l1 c0) (has-color b1 l2 c0) (has-color b1 l3 c0) (has-color b1 l4 c0))
      (and (has-color b2 l1 c0) (has-color b2 l2 c0) (has-color b2 l3 c0) (has-color b2 l4 c0))
      (and (has-color b3 l1 c0) (has-color b3 l2 c0) (has-color b3 l3 c0) (has-color b3 l4 c0))
      (and (has-color b4 l1 c0) (has-color b4 l2 c0) (has-color b4 l3 c0) (has-color b4 l4 c0))
      (and (has-color b5 l1 c0) (has-color b5 l2 c0) (has-color b5 l3 c0) (has-color b5 l4 c0))
      (and (has-color b6 l1 c0) (has-color b6 l2 c0) (has-color b6 l3 c0) (has-color b6 l4 c0))
    )
    ; Goal for color c1
    (or
      (and (has-color b0 l1 c1) (has-color b0 l2 c1) (has-color b0 l3 c1) (has-color b0 l4 c1))
      (and (has-color b1 l1 c1) (has-color b1 l2 c1) (has-color b1 l3 c1) (has-color b1 l4 c1))
      (and (has-color b2 l1 c1) (has-color b2 l2 c1) (has-color b2 l3 c1) (has-color b2 l4 c1))
      (and (has-color b3 l1 c1) (has-color b3 l2 c1) (has-color b3 l3 c1) (has-color b3 l4 c1))
      (and (has-color b4 l1 c1) (has-color b4 l2 c1) (has-color b4 l3 c1) (has-color b4 l4 c1))
      (and (has-color b5 l1 c1) (has-color b5 l2 c1) (has-color b5 l3 c1) (has-color b5 l4 c1))
      (and (has-color b6 l1 c1) (has-color b6 l2 c1) (has-color b6 l3 c1) (has-color b6 l4 c1))
    )
    ; Goal for color c2
    (or
      (and (has-color b0 l1 c2) (has-color b0 l2 c2) (has-color b0 l3 c2) (has-color b0 l4 c2))
      (and (has-color b1 l1 c2) (has-color b1 l2 c2) (has-color b1 l3 c2) (has-color b1 l4 c2))
      (and (has-color b2 l1 c2) (has-color b2 l2 c2) (has-color b2 l3 c2) (has-color b2 l4 c2))
      (and (has-color b3 l1 c2) (has-color b3 l2 c2) (has-color b3 l3 c2) (has-color b3 l4 c2))
      (and (has-color b4 l1 c2) (has-color b4 l2 c2) (has-color b4 l3 c2) (has-color b4 l4 c2))
      (and (has-color b5 l1 c2) (has-color b5 l2 c2) (has-color b5 l3 c2) (has-color b5 l4 c2))
      (and (has-color b6 l1 c2) (has-color b6 l2 c2) (has-color b6 l3 c2) (has-color b6 l4 c2))
    )
    ; Goal for color c3
    (or
      (and (has-color b0 l1 c3) (has-color b0 l2 c3) (has-color b0 l3 c3) (has-color b0 l4 c3))
      (and (has-color b1 l1 c3) (has-color b1 l2 c3) (has-color b1 l3 c3) (has-color b1 l4 c3))
      (and (has-color b2 l1 c3) (has-color b2 l2 c3) (has-color b2 l3 c3) (has-color b2 l4 c3))
      (and (has-color b3 l1 c3) (has-color b3 l2 c3) (has-color b3 l3 c3) (has-color b3 l4 c3))
      (and (has-color b4 l1 c3) (has-color b4 l2 c3) (has-color b4 l3 c3) (has-color b4 l4 c3))
      (and (has-color b5 l1 c3) (has-color b5 l2 c3) (has-color b5 l3 c3) (has-color b5 l4 c3))
      (and (has-color b6 l1 c3) (has-color b6 l2 c3) (has-color b6 l3 c3) (has-color b6 l4 c3))
    )
    ; Goal for color c4
    (or
      (and (has-color b0 l1 c4) (has-color b0 l2 c4) (has-color b0 l3 c4) (has-color b0 l4 c4))
      (and (has-color b1 l1 c4) (has-color b1 l2 c4) (has-color b1 l3 c4) (has-color b1 l4 c4))
      (and (has-color b2 l1 c4) (has-color b2 l2 c4) (has-color b2 l3 c4) (has-color b2 l4 c4))
      (and (has-color b3 l1 c4) (has-color b3 l2 c4) (has-color b3 l3 c4) (has-color b3 l4 c4))
      (and (has-color b4 l1 c4) (has-color b4 l2 c4) (has-color b4 l3 c4) (has-color b4 l4 c4))
      (and (has-color b5 l1 c4) (has-color b5 l2 c4) (has-color b5 l3 c4) (has-color b5 l4 c4))
      (and (has-color b6 l1 c4) (has-color b6 l2 c4) (has-color b6 l3 c4) (has-color b6 l4 c4))
    )
  ))
)