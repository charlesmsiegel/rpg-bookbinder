// =============================================================================
// REFRACTION — generative cover algorithm for PRISM
//
// One achromatic beam enters a perturbed medium and leaves as spectrum.
// Nothing is painted. Colour is computed from wavelength, direction is computed
// from Snell's law, and brightness is the density of accumulated sub-rays in a
// floating-point light buffer.
// =============================================================================

const params = {
  seed: 20260826,

  // canvas
  W: 1600,
  H: 2400,

  // the beam
  beamX: 0.50,          // column centre, fraction of width
  beamTop: 0.045,       // where the beam becomes visible
  beamHalfWidth: 46,    // px
  boundaryY: 0.400,     // where the medium begins, fraction of height

  // the medium
  incidence: 0.86,      // theta_in from the normal, radians (~49 deg)
  cauchyA: 1.500,       // n(lambda) = A + B / lambda^2, lambda in microns
  cauchyB: 0.00460,
  dispersionGain: 90.0, // scales the angular disagreement to canvas scale

  // sampling
  wavelengths: 260,
  subRays: 120,         // per wavelength
  stepLen: 1.25,
  rippleAmp: 92.0,      // lateral noise displacement in the fan, px
  noiseScale: 0.00085,

  // the five
  spineBoost: 1.85,
  spineWidth: 5.0,      // nm

  // finishing
  bloomRadius: 26,
  bloomAmount: 0.55,
  exposure: 1.75,
  gamma: 0.78,
  dust: 1100,
};

// The five Stars, as the nearest spectral wavelengths to their colours.
const SPINES = [
  { nm: 404, name: 'violet' },
  { nm: 492, name: 'cyan' },
  { nm: 516, name: 'mint' },
  { nm: 578, name: 'sunburst yellow' },
  { nm: 660, name: 'magenta' },
];

let buf; // Float32Array, W*H*3 — additive light

// ---------------------------------------------------------------- wavelength
// Visible-spectrum approximation: nanometres in, linear RGB out.
function wavelengthRGB(nm) {
  let r = 0, g = 0, b = 0;
  if (nm >= 380 && nm < 440)       { r = -(nm - 440) / 60;  g = 0; b = 1; }
  else if (nm >= 440 && nm < 490)  { r = 0; g = (nm - 440) / 50; b = 1; }
  else if (nm >= 490 && nm < 510)  { r = 0; g = 1; b = -(nm - 510) / 20; }
  else if (nm >= 510 && nm < 580)  { r = (nm - 510) / 70; g = 1; b = 0; }
  else if (nm >= 580 && nm < 645)  { r = 1; g = -(nm - 645) / 65; b = 0; }
  else if (nm >= 645 && nm <= 780) { r = 1; g = 0; b = 0; }

  // Eye response falls off at both ends; keep more than the textbook curve so
  // the extremes of the fan stay present rather than fading to nothing.
  let f = 1;
  if (nm >= 380 && nm < 420)       f = 0.35 + 0.65 * (nm - 380) / 40;
  else if (nm > 700 && nm <= 780)  f = 0.35 + 0.65 * (780 - nm) / 80;
  return [r * f, g * f, b * f];
}

function refractiveIndex(nm) {
  const um = nm / 1000;
  return params.cauchyA + params.cauchyB / (um * um);
}

// ------------------------------------------------------------------ deposit
function deposit(x, y, r, g, b, w) {
  const W = params.W, H = params.H;
  const xi = x | 0, yi = y | 0;
  if (xi < 1 || yi < 1 || xi >= W - 1 || yi >= H - 1) return;
  const fx = x - xi, fy = y - yi;
  for (let dy = 0; dy <= 1; dy++) {
    for (let dx = 0; dx <= 1; dx++) {
      const wgt = w * (dx ? fx : 1 - fx) * (dy ? fy : 1 - fy);
      const i = ((yi + dy) * W + (xi + dx)) * 3;
      buf[i] += r * wgt;
      buf[i + 1] += g * wgt;
      buf[i + 2] += b * wgt;
    }
  }
}

// ------------------------------------------------------------------- tracing
// The approach: one achromatic column, hot at the boundary, no separation yet.
function traceApproach() {
  const W = params.W, H = params.H;
  const cx = params.beamX * W;
  const by = params.boundaryY * H;
  const topY = params.beamTop * H;

  for (let y = topY; y < by; y += 1) {
    const ramp = Math.pow((y - topY) / (by - topY), 1.35);
    const hw = params.beamHalfWidth * (0.50 + 0.50 * ramp);
    const amp = (0.22 + 1.9 * ramp) * 0.018;
    for (let s = 0; s < 170; s++) {
      const u = randomGaussian(0, 0.44);
      if (Math.abs(u) > 1.7) continue;
      const wob = (noise(y * 0.0055, s * 0.013, 3.1) - 0.5) * 5;
      deposit(cx + u * hw + wob, y, amp * Math.exp(-u * u * 1.5),
                                   amp * Math.exp(-u * u * 1.5),
                                   amp * Math.exp(-u * u * 1.5), 1);
    }
  }
}

// The fan: wavelengths that agreed all the way down stop agreeing at the
// boundary. Direction is fixed downward; the disagreement is entirely lateral,
// so the fan opens monotonically and can only braid, never converge.
function traceFan() {
  const W = params.W, H = params.H;
  const cx = params.beamX * W;
  const by = params.boundaryY * H;
  const run = H - by;

  const sinIn = Math.sin(params.incidence);
  const thetaMid = Math.asin(Math.min(1, sinIn / refractiveIndex(540)));

  for (let wi = 0; wi < params.wavelengths; wi++) {
    const t = wi / (params.wavelengths - 1);
    const nm = 380 + t * 320;
    const [cr, cg, cb] = wavelengthRGB(nm);

    // Snell, then scale the angular disagreement to canvas scale.
    const theta = Math.asin(Math.min(1, sinIn / refractiveIndex(nm)));
    const slope = (theta - thetaMid) * params.dispersionGain;

    // The five spines persist a little further than their neighbours.
    let boost = 1;
    for (const sp of SPINES) {
      const d = (nm - sp.nm) / params.spineWidth;
      boost += (params.spineBoost - 1) * Math.exp(-d * d);
    }

    for (let s = 0; s < params.subRays; s++) {
      const u = randomGaussian(0, 0.45);
      if (Math.abs(u) > 1.7) continue;
      const x0 = cx + u * params.beamHalfWidth;

      // the interface is not a clean plane
      const y0 = by + (noise(x0 * 0.0026, nm * 0.004, 900.0) - 0.5) * 44;

      const weight = 0.0255 * (params.stepLen / 3.0) * boost * Math.exp(-u * u * 1.2);

      // random phase per sub-ray, so the discrete march leaves no scan lines
      for (let d = random(0, params.stepLen); d < run + 40; d += params.stepLen) {
        const py = y0 + d;
        if (py >= H) break;
        const g = d / run;                       // 0 at the boundary, 1 at the foot
        // Each wavelength wanders on its own noise thread, so neighbouring
        // bands cross and braid instead of translating together.
        const rip = (noise(nm * 0.021, py * params.noiseScale * 1.7, 77.0) - 0.5)
                  * params.rippleAmp * g
                  + (noise(nm * 0.058, py * params.noiseScale * 4.3, 41.3) - 0.5)
                  * params.rippleAmp * 0.40 * g
                  + (noise(x0 * 0.0012, py * params.noiseScale * 1.6, 11.7) - 0.5)
                  * params.rippleAmp * 0.35 * g;
        const px = x0 + slope * d + rip;
        // same light over a widening area: dim as it opens
        const fade = 1 / (1 + 2.1 * g);
        deposit(px, py, cr * weight * fade, cg * weight * fade, cb * weight * fade, 1);
      }
    }
  }
}

// --------------------------------------------------------------------- dust
function traceDust() {
  const W = params.W, H = params.H;
  for (let i = 0; i < params.dust; i++) {
    const x = random(W);
    const y = random(H);
    const r = random(0.6, 2.6);
    const a = random(0.05, 0.55);
    for (let k = 0; k < 22; k++) {
      const ang = random(TWO_PI);
      const rr = random(r);
      deposit(x + Math.cos(ang) * rr, y + Math.sin(ang) * rr, a, a, a, 0.08);
    }
  }
}

// -------------------------------------------------------------------- bloom
// Separable box blur, three passes, applied to the light buffer and added back.
// Glow is light that scattered, so it belongs in the buffer, not on the pixels.
function bloom() {
  const W = params.W, H = params.H, R = params.bloomRadius;
  const n = W * H * 3;
  let a = new Float32Array(buf);
  let b = new Float32Array(n);

  for (let pass = 0; pass < 3; pass++) {
    // horizontal
    for (let y = 0; y < H; y++) {
      for (let c = 0; c < 3; c++) {
        let acc = 0;
        const row = y * W;
        for (let x = -R; x <= R; x++) acc += a[(row + Math.min(W - 1, Math.max(0, x))) * 3 + c];
        const inv = 1 / (2 * R + 1);
        for (let x = 0; x < W; x++) {
          b[(row + x) * 3 + c] = acc * inv;
          const add = Math.min(W - 1, x + R + 1), sub = Math.max(0, x - R);
          acc += a[(row + add) * 3 + c] - a[(row + sub) * 3 + c];
        }
      }
    }
    // vertical
    for (let x = 0; x < W; x++) {
      for (let c = 0; c < 3; c++) {
        let acc = 0;
        for (let y = -R; y <= R; y++) acc += b[(Math.min(H - 1, Math.max(0, y)) * W + x) * 3 + c];
        const inv = 1 / (2 * R + 1);
        for (let y = 0; y < H; y++) {
          a[(y * W + x) * 3 + c] = acc * inv;
          const add = Math.min(H - 1, y + R + 1), sub = Math.max(0, y - R);
          acc += b[(add * W + x) * 3 + c] - b[(sub * W + x) * 3 + c];
        }
      }
    }
  }

  const k = params.bloomAmount;
  for (let i = 0; i < n; i++) buf[i] += a[i] * k;
}

// ------------------------------------------------------------------- render
function tonemap() {
  const W = params.W, H = params.H;
  loadPixels();
  const px = pixels;
  const e = params.exposure, gm = params.gamma;
  for (let i = 0, p = 0; i < W * H * 3; i += 3, p += 4) {
    // deep violet ground, so the frame is never flat black
    const yFrac = ((i / 3) / W) / H;
    const groundR = 10 + 12 * (1 - yFrac);
    const groundG = 3 + 4 * (1 - yFrac);
    const groundB = 26 + 30 * (1 - yFrac);

    const r = 1 - Math.exp(-buf[i] * e);
    const g = 1 - Math.exp(-buf[i + 1] * e);
    const b = 1 - Math.exp(-buf[i + 2] * e);

    // ordered dither, so the long slow ground gradient does not band
    const d = (((i / 3) % 7) * 0.14 + (((i / 3) / W | 0) % 5) * 0.19) - 0.55;
    px[p]     = Math.min(255, groundR + d + 255 * Math.pow(r, gm));
    px[p + 1] = Math.min(255, groundG + d + 255 * Math.pow(g, gm));
    px[p + 2] = Math.min(255, groundB + d + 255 * Math.pow(b, gm));
    px[p + 3] = 255;
  }
  updatePixels();
}

function drawTitle() {
  const W = params.W, H = params.H;

  textAlign(CENTER, CENTER);
  textFont('DejaVu Sans');
  textStyle(BOLD);

  // PRISM — letter-spaced by hand so the beam appears to come out of the word
  const title = 'PRISM';
  const size = 250;
  textSize(size);
  const tracking = 44;
  let total = 0;
  for (const ch of title) total += textWidth(ch) + tracking;
  total -= tracking;

  const baseY = H * 0.128;
  let x = W / 2 - total / 2;

  // soft halo first
  for (const ch of title) {
    const w = textWidth(ch);
    fill(255, 255, 255, 26);
    for (let k = 1; k <= 5; k++) {
      textSize(size + k * 5);
      text(ch, x + w / 2, baseY);
    }
    textSize(size);
    x += w + tracking;
  }

  x = W / 2 - total / 2;
  for (const ch of title) {
    const w = textWidth(ch);
    fill(255);
    text(ch, x + w / 2, baseY);
    x += w + tracking;
  }

  // rule
  stroke(255, 120);
  strokeWeight(3);
  line(W / 2 - total / 2, baseY + size * 0.62, W / 2 + total / 2, baseY + size * 0.62);
  noStroke();

  textStyle(NORMAL);
  textSize(52);
  fill(255, 215);
  text('SPLIT  THE  LIGHT', W / 2, baseY + size * 0.62 + 62);

  // a scrim so the footer stays legible wherever the fan lands
  noStroke();
  for (let i = 0; i < 90; i++) {
    fill(8, 3, 22, 3.0 * (i / 90));
    rect(0, H - 90 + i, W, 1);
  }
  textSize(34);
  fill(255, 175);
  text('A TABLETOP ROLEPLAYING GAME', W / 2, H * 0.962);
}

// --------------------------------------------------------------------- p5
function setup() {
  createCanvas(params.W, params.H);
  pixelDensity(1);
  randomSeed(params.seed);
  noiseSeed(params.seed);
  noiseDetail(4, 0.5);

  buf = new Float32Array(params.W * params.H * 3);

  traceApproach();
  traceFan();
  traceDust();
  bloom();
  tonemap();
  drawTitle();

  noLoop();
  window.__coverReady = true;
}
