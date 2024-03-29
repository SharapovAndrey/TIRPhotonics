## Transmission modeling (implemented on wxMaxima)

### References:

[1] Max Born and Emil Wolf. Principles of Optics. 6th Edition. Electromagnetic Theory of Propagation, Interference and Diffraction of Light

[2] Alyabyeva et al. Dielectric properties of semiinsulating Fe-doped InP in the THz spectral region, 2017

[3] Dai et al. Measurement of optical constants of TiN and TiN/Ti/TiN mulitlayer films for microwave kinetic inductance photon-number-resolving detectors, 2018

### Stages:

1. Final formula of reflectivity and transmissivity ([1], 1.6.4, formulae 54-60, p. 61-62, "RT dielectric film.wxmx")

2. Reproduction of Fig. 1 in [2], 

    2.1. "RT dielectric film verification.wxmx"

    2.2. "RT dielectric film matrix.wxmx" -- the same as 2.1, but using characteristic matrix of the film ([1], 1.6.2, formulae ~39, p. ~58), i.e. transfer matrix method (TMM) for dielectric films

3. Reproduction of Fig. 3a in [3], "ART TiN-Ti-TiN film verification.wxmx", i.e. TMM for arbitrary films

4. Optimization of Ti thickness film on Si substrate for maximum transmittance
