# VLQ Open-Data Knowledge Notes

## Reducible Backgrounds: Fake/Non-Prompt Leptons

Source checked: `analysis/ATLAS VLQ.pdf`, Section 7, plus the local open-data
files under:

- `/global/cfs/projectdirs/atlas/haichen/opendata/1lepMET30/data`
- `/global/cfs/projectdirs/atlas/haichen/opendata/1lepMET30/MC`

The paper estimates the fake/non-prompt lepton background with a matrix method.
It defines:

- `r`: probability that a prompt lepton passing the relaxed selection also
  passes the nominal selection.
- `f`: probability that a fake/non-prompt lepton passing the relaxed selection
  also passes the nominal selection.

The relevant paper selections are:

- Electron relaxed: medium likelihood ID, no isolation.
- Electron nominal: tight likelihood ID plus track and calorimeter isolation.
- Muon relaxed: medium ID, no isolation.
- Muon nominal: medium ID plus track isolation.
- Electron prompt-control region for `r`: single-electron events with
  `ETmiss > 150 GeV`, dominated by `W -> e nu`.
- Electron fake-control region for `f`: single-electron events with
  `mT(W) < 20 GeV` and `ETmiss + mT(W) < 60 GeV`, dominated by multijet and
  heavy-flavour fake electrons.
- Muon prompt-control region for `r`: single-muon events with `mT(W) > 100 GeV`,
  dominated by `W -> mu nu`.
- Muon fake-control region for `f`: single-muon events with
  `|d0 significance| > 5`, targeting heavy-flavour muons.

The paper parameterizes `r` and `f` using lepton flavour, lepton `pT`, lepton
`|eta|`, angular distance to the nearest jet, and number of b-tagged jets. It
also subtracts prompt-lepton MC contamination from the fake-control samples.

## Local Open-Data Feasibility

The local 1-lepton-plus-MET data stream has 16 data ROOT files. The branches are
rich enough to build a paper-inspired loose-to-tight proxy:

- `lep_type`
- `lep_pt`, `lep_eta`, `lep_phi`
- `lep_charge`
- `lep_isMediumID`
- `lep_isTightID`
- `lep_isLooseIso`, `lep_isTightIso`
- `lep_ptvarcone30`, `lep_topoetcone20`
- `lep_d0sig`, `lep_z0`
- `met`, `met_phi`
- `jet_pt`, `jet_eta`, `jet_phi`
- `jet_btag_quantile`

Pilot scan over the first 50,000 entries of each data file, 800,000 events
total, using explicit ID/isolation branches rather than the already-tight
`sig_lep` mask:

- Electron prompt CR proxy, `ETmiss > 150 GeV`:
  `nominal / relaxed ~= 0.86`.
- Electron fake CR proxy, `mT(W) < 20 GeV` and `ETmiss + mT(W) < 60 GeV`:
  `nominal / relaxed ~= 0.32`.
- Muon prompt CR proxy, `mT(W) > 100 GeV`:
  `nominal / relaxed ~= 0.95`.
- Muon fake CR using the paper's `|d0 significance| > 5` requirement:
  no candidates in the pilot scan.

The muon fake-control issue appears to be a skim limitation: sampled muons have
`|lep_d0sig| < 3`, so the official `|d0 significance| > 5` fake-enriched muon
control region is not available in this open-data stream.

## Recommended Policy

Implementing an official reproduction of the paper matrix method is not
supported by the available files, because the exact efficiency maps, binning,
prompt-subtraction details, and full systematic treatment are not provided.

An open-data proxy is still useful and should be labelled clearly:

1. Build a separate relaxed/nominal lepton selector for fake-rate studies. Do
   not use `sig_lep` as the relaxed category, because it behaves like an
   already-tight signal-lepton mask.
2. Measure electron `r` and `f` from the paper-like single-lepton data control
   regions.
3. Measure muon `r` from the paper-like `mT(W) > 100 GeV` control region.
4. Treat muon `f` as blocked by the open-data skim if using the paper's
   `|d0 significance| > 5` control region. Use either an explicitly labelled
   alternate anti-isolation/low-`mT` proxy or the paper's quoted `7-30%` range
   as an external systematic.
5. Subtract prompt MC contamination from fake-control regions where possible.
6. Parameterize rates at least by lepton flavour and coarse lepton `pT`/`|eta|`
   bins; add nearest-jet `DeltaR` and `n_btags` bins only if control-region
   statistics remain stable.
7. Report results as an "open-data fake-rate proxy" or "paper-inspired matrix
   method proxy", not as the official ATLAS fake/non-prompt estimate.

## Charge Misidentification

The paper measures electron charge-misidentification probabilities in
`Z -> ee` data, binned in electron `pT` and `|eta|`, after subtracting the
fake/non-prompt electron contribution with the matrix method. It then applies
these probabilities to opposite-charge `ee` and `e mu` events passing the
analysis selections.

The local data has enough electron kinematics and charge information to define a
`Z -> ee` control proxy and opposite-charge application region, but it does not
provide the official charge-flip probability maps or the exact fake-subtraction
machinery. Any charge-misID estimate should therefore be treated as a proxy or
as an external paper-constrained input.

## Generator and Alternative-Sample Policy

The paper documents both nominal MC generators and modeling-uncertainty
procedures. The important implementation rule is that different generator,
shower, radiation, or systematic-variation samples are not separate physics
backgrounds to be summed together. They are alternative descriptions of the same
process and should be used for uncertainty or diagnostic comparisons unless an
explicit central-sample policy promotes them.

Paper nominal signal generation:

- Vector-like `T`, `B`, and `T5/3` pair production: Protos v2.2 plus
  Pythia 8.186 for showering/hadronisation, NNPDF2.3LO PDFs, with VLQ masses
  from 0.50 to 1.40 TeV.
- SM four-top production: MG5_aMC@NLO v2.2.2 plus Pythia 8.186, NNPDF2.3LO.
- 2UED/RPP four-top signal: Pythia 8.186, NNPDF2.3LO.
- Contact-interaction four-top signal: MG5_aMC@NLO v2.2.3 plus Pythia 8.205,
  NNPDF2.3LO.
- Same-sign top-quark pair production: MG5_aMC@NLO v2.3.3 plus Pythia 8.210,
  NNPDF2.3LO.

Paper nominal irreducible-background generation:

- `ttV`, `ttH`, `ttt`, `tttt`, `ttWW`, and `tZW`: MG5_aMC@NLO v2.2.2 plus
  Pythia 8.186, NNPDF3.0NLO. NLO matrix elements are used for `ttV`, `ttH`,
  and `tZW`; LO matrix elements are used for `ttt`, `tttt`, and `ttWW`.
- `tZ`: MG5_aMC@NLO v2.2.2 with LO matrix element plus Pythia 6.428,
  CTEQ6L1 PDFs, and Perugia2012 tune.
- Diboson and triboson: Sherpa v2.2.1 with Comix/OpenLoops matrix elements
  merged with the Sherpa parton shower using ME+PS@NLO.
- `VH`: Pythia 8.186, NNPDF2.3LO.
- EvtGen v1.2 is used for charm and bottom hadron decays for all samples except
  Sherpa samples. The A14 tune is used unless otherwise stated.

Paper modeling-uncertainty treatment:

- For `ttW` and `ttZ`, background-model uncertainties are evaluated by varying
  renormalisation and factorisation scales by factors of two and by comparing
  nominal MG5_aMC@NLO samples with Sherpa v2.2.1 samples.
- For diboson production, uncertainties are evaluated by varying
  renormalisation, factorisation, and resummation scales by factors of two and
  by changing the CKKW merging scale to 15 and 30 GeV around a nominal 20 GeV.
- The paper quotes cross-section uncertainties of about 13% for `ttW`, 12% for
  `ttZ`, 6% for diboson, and asymmetric uncertainty for `ttH`; other
  irreducible backgrounds are assigned 50% of the nominal yield.

Local open-data implication:

- Available local samples include nominal-like `ttW`, `ttZ`, many `ttH`
  channels, Sherpa diboson/triboson samples, and two SM four-top generator
  variants (`412043` Pythia and `412044` Herwig).
- Local files with tokens such as `Herwig`, `H7UE`, `ShowerSys`, `_shw`,
  `pThard`, `DS_dyn`, or explicit Sherpa-vs-aMC alternatives should be marked
  as noncentral alternatives unless a revised contract says otherwise.
- Do not add nominal and alternative generator/shower samples for the same
  process into the same central background total. This would double count the
  process and inflate expected yields.
- For the central diagnostic result, pick one nominal representation per
  process or exclusive decay slice, then retain alternatives in accounting
  artifacts for modeling/systematic comparisons.
