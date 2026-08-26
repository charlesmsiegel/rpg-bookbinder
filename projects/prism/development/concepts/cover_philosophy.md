# Refraction — an algorithmic philosophy for the PRISM cover

## The movement

**Refraction** holds that colour is not added to the world. Colour is already
in the world, travelling as one indivisible white beam, and all a prism does is
slow it down enough that the wavelengths stop agreeing with each other. Nothing
is created at the boundary. Something that was always there is finally
separated enough to be seen.

This is the computational worldview the algorithm expresses. It does not paint
a rainbow onto a dark field. It launches a single achromatic beam, gives the
medium a dispersion coefficient, and lets the spectrum *emerge* from the angular
disagreement between wavelengths. Every band on the finished canvas is the
consequence of one number — the refractive index at that wavelength — applied
with the patience of a meticulously crafted algorithm. The beauty is in the
process. The frame is only where the process stopped.

## Algorithmic expression

The system is a single ray tracer with no scene. A beam of N sampled
wavelengths enters from the upper region of the canvas travelling as one line,
strikes an implicit boundary, and refracts. Snell's law does the work:
`sin(theta_out) = sin(theta_in) / n(lambda)`, where `n` falls smoothly across
the visible band. Wavelengths that were coincident for the whole approach
diverge by fractions of a degree at the interface and then, over two thousand
pixels of travel, fan into a full spectrum. The fan is not drawn. It is
integrated, step by step, as thousands of sub-rays accumulate additive light
into a floating-point buffer.

Layered value noise perturbs the medium so the boundary is not a clean plane.
This is the painstaking part, and where the master-level implementation shows:
a perfectly flat interface produces a textbook diagram, and a fully turbulent
one produces mud. The tuned regime sits between them — enough perturbation that
the bands ripple and braid where they cross, little enough that the spectral
order survives from deep red at one edge to violet at the other. Every octave
weight in that noise stack was chosen by someone who has looked at a great many
failed versions.

Colour is never sampled from a palette. Each ray carries a wavelength in
nanometres, and its RGB is computed from that wavelength alone by a standard
visible-spectrum approximation. The palette of the finished piece is therefore
not a decision. It is physics, run at high sample count, and the saturation of
the result comes from additive accumulation rather than from choosing bright
paint. This is what separates a computational aesthetic from a decorative one.

Density becomes brightness. Where many sub-rays cross the same cell, the buffer
saturates toward white, so the beam before the boundary reads as hot achromatic
light and the fan after it reads as separated colour, exactly as it should. A
final tone curve and a faint particle field — dust in the beam path, seeded from
the same generator — finish the composition without being asked to carry it.

## The conceptual seed

Five wavelengths in the sampled set are weighted slightly heavier than their
neighbours. They are the spectral wavelengths nearest the five Stars' colours,
and they are the only hand-placed numbers in the entire algorithm. Nothing on
the canvas announces them. They simply persist a little further into the fan
than the wavelengths on either side, so the spectrum has five faint spines
running through it.

Someone who has read the book will know why there are five. Everyone else sees
white light becoming colour, which is the other true thing about this game.

## Reproducibility

Seeded throughout (`seed = 20260826`). The same seed produces the same canvas
on any machine. Re-running with a different seed re-rolls the noise field and
the dust, and produces a different but equally valid member of the movement.
