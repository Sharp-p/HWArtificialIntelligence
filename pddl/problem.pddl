(define (problem liquidsort_task)
  (:domain LiquidSort)
  (:objects
    b0 b1 b2 - beaker
    c0 c1 - color
    l0 l1 l2 - level
  )

  (:init
    ; --- Geometry of the game (static) ---
    (is-bottom l0)
    (succ l0 l1)
    (succ l1 l2)

    ; --- Defining initial state of the beakers ---
    (has-color b0 l1 c0)
    (has-color b0 l2 c1)
    (top b0 l2)
    (has-color b1 l1 c1)
    (has-color b1 l2 c0)
    (top b1 l2)
    (top b2 l0)
  )

  (:goal (and
    ; Goal for color c0
    (or
      (and (has-color b0 l1 c0) (has-color b0 l2 c0))
      (and (has-color b1 l1 c0) (has-color b1 l2 c0))
      (and (has-color b2 l1 c0) (has-color b2 l2 c0))
    )
    ; Goal for color c1
    (or
      (and (has-color b0 l1 c1) (has-color b0 l2 c1))
      (and (has-color b1 l1 c1) (has-color b1 l2 c1))
      (and (has-color b2 l1 c1) (has-color b2 l2 c1))
    )
  ))
)