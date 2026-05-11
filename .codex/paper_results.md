# Paper Results Reference

Source: `analysis/ATLAS VLQ.pdf`, ATLAS same-charge leptons plus b-jets paper
(`JHEP 12 (2018) 039`, arXiv:1807.11883), 36.1 fb-1 at 13 TeV.

This document collects paper-level numbers that an agent can compare against
open-data outputs. The paper does not publish a conventional full cutflow table.
It publishes object/region definitions, preselection and signal-region
efficiencies for selected signal models, validation-region yields, signal-region
yields, systematic uncertainty summaries, and final limits.

## Comparison Scope

- Directly comparable:
  - Region definitions.
  - Observed event counts in validation and signal regions.
  - Total expected background yields by region.
  - Major background composition by region, if the agent implements matching
    background categories.
  - Selection efficiencies only for the paper's generated signal samples.
- Not directly comparable without dedicated paper inputs:
  - Full event cutflow: not published in the paper.
  - Official VLQ mass limits: require missing dedicated VLQ signal grids.
  - Official fake/non-prompt and charge-misID estimates: require missing
    official efficiency/probability maps and nuisance model.
  - Full CLs/profile-likelihood limits: require the paper likelihood and
    correlated nuisance model.

## Object And Preselection Summary

Paper object thresholds:

- Electrons: `pT > 28 GeV`, `|eta| < 2.47`, excluding `1.37 < |eta| < 1.52`.
  In `ee` and `e mu` channels, electrons with `|eta| > 1.37` are not used.
- Muons: `pT > 28 GeV`, `|eta| < 2.5`.
- Jets: `pT > 25 GeV`, `|eta| < 2.5`.
- b-jets: paper uses a 77% b-tagging working point.
- Same-charge dilepton preselection: at least one jet and exactly two nominal
  leptons among the three highest-pT leptons, with same charge. Same-charge
  `ee` events require `m_ee > 15 GeV` and `|m_ee - 91 GeV| > 10 GeV`.
- Trilepton preselection: at least one jet and three nominal leptons among the
  three highest-pT leptons. No lepton charge or pair-mass requirement.

## Region Definitions: VLQ And Four-Top

All two-lepton regions require same-charge leptons (`++` or `--`). Three-lepton
regions have no charge requirement.

| Region | Njets | Nbtags | Nlep | Charge | Kinematic criteria |
| --- | ---: | ---: | ---: | --- | --- |
| `VR1b2l` | >=1 | 1 | 2 | same charge | `400 < HT < 2400 GeV` or `ETmiss < 40 GeV` |
| `SR1b2l` | >=1 | 1 | 2 | same charge | `HT > 1000 GeV` and `ETmiss > 180 GeV` |
| `VR2b2l` | >=2 | 2 | 2 | same charge | `HT > 400 GeV` |
| `SR2b2l` | >=2 | 2 | 2 | same charge | `HT > 1200 GeV` and `ETmiss > 40 GeV` |
| `VR3b2l` | >=3 | >=3 | 2 | same charge | `400 < HT < 1400 GeV` or `ETmiss < 40 GeV` |
| `SR3b2l_L` | >=7 | >=3 | 2 | same charge | `500 < HT < 1200 GeV` and `ETmiss > 40 GeV` |
| `SR3b2l` | >=3 | >=3 | 2 | same charge | `HT > 1200 GeV` and `ETmiss > 100 GeV` |
| `VR1b3l` | >=1 | 1 | 3 | any | `400 < HT < 2000 GeV` or `ETmiss < 40 GeV` |
| `SR1b3l` | >=1 | 1 | 3 | any | `HT > 1000 GeV` and `ETmiss > 140 GeV` |
| `VR2b3l` | >=2 | 2 | 3 | any | `400 < HT < 2400 GeV` or `ETmiss < 40 GeV` |
| `SR2b3l` | >=2 | 2 | 3 | any | `HT > 1200 GeV` and `ETmiss > 100 GeV` |
| `VR3b3l` | >=3 | >=3 | 3 | any | `HT > 400 GeV` |
| `SR3b3l_L` | >=5 | >=3 | 3 | any | `500 < HT < 1000 GeV` and `ETmiss > 40 GeV` |
| `SR3b3l` | >=3 | >=3 | 3 | any | `HT > 1000 GeV` and `ETmiss > 40 GeV` |

Validation regions veto events that appear in any signal region.

## Region Definitions: Same-Sign Top

| Region | Nbtags | Nlep | HT | ETmiss | Delta phi ll | Lepton flavour/charge |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `VRtt` | >=1 | 2 | >750 GeV | >40 GeV | >2.5 | `e-e-`, `e-mu-`, or `mu-mu-` |
| `SRttee` | >=1 | 2 | >750 GeV | >40 GeV | >2.5 | `e+e+` |
| `SRttemu` | >=1 | 2 | >750 GeV | >40 GeV | >2.5 | `e+mu+` |
| `SRttmumu` | >=1 | 2 | >750 GeV | >40 GeV | >2.5 | `mu+mu+` |

## Published Signal Efficiencies

The paper reports preselection efficiencies and signal-region efficiencies for
selected signal models. These are MC efficiencies in percent. The paired entries
for VLQ/four-top are `2l / 3l`.

| Signal | Preselection [%] | SR1b 2l/3l [%] | SR2b 2l/3l [%] | SR3b_L 2l/3l [%] | SR3b 2l/3l [%] |
| --- | ---: | ---: | ---: | ---: | ---: |
| `B Bbar`, `mB = 800 GeV` | 1.7 | 0.12 / 0.16 | 0.19 / 0.14 | 0.007 / 0.002 | 0.05 / 0.04 |
| `B Bbar`, `mB = 1200 GeV` | 1.9 | 0.27 / 0.28 | 0.31 / 0.24 | `4e-4 / 4e-4` | 0.07 / 0.05 |
| `T Tbar`, `mT = 800 GeV` | 1.2 | 0.06 / 0.02 | 0.09 / 0.02 | 0.008 / 0.006 | 0.04 / 0.06 |
| `T Tbar`, `mT = 1200 GeV` | 1.3 | 0.10 / 0.25 | 0.13 / 0.22 | 0.002 / `9e-4` | 0.06 / 0.11 |
| SM four-top | 2.7 | 0.02 / 0.02 | 0.11 / 0.04 | 0.37 / 0.17 | 0.20 / 0.18 |
| CI four-top | 3.0 | 0.06 / 0.05 | 0.23 / 0.08 | 0.30 / 0.16 | 0.33 / 0.27 |
| 2HDM four-top, `mH = 700 GeV` | 3.1 | 0.02 / 0.03 | 0.11 / 0.03 | 0.62 / 0.24 | 0.19 / 0.17 |
| 2UED/RPP four-top, `mKK = 1400 GeV` | 3.3 | 0.27 / 0.16 | 0.62 / 0.31 | `8e-4 / 0.0` | 0.89 / 0.51 |

Same-sign top signal efficiencies:

| Signal | Preselection [%] | SRttee [%] | SRttemu [%] | SRttmumu [%] |
| --- | ---: | ---: | ---: | ---: |
| `tt`, `mV = 2000 GeV` | 2.0 | 0.1 | 0.3 | 0.3 |
| `tt ubar` off-shell, `mV = 2000 GeV` | 1.7 | 0.1 | 0.2 | 0.2 |
| `tV -> t ubar` on-shell, `mV = 2000 GeV` | 1.8 | 0.04 | 0.2 | 0.1 |

## Validation Region Yields: VLQ And Four-Top

Uncertainties are statistical then systematic.

| Source | VR1b2l | VR2b2l | VR3b2l |
| --- | ---: | ---: | ---: |
| ttW | `49 +/- 1 +/- 14` | `48 +/- 1 +/- 13` | `5.8 +/- 0.3 +/- 2.8` |
| ttZ | `28.7 +/- 0.5 +/- 4.6` | `27.6 +/- 0.4 +/- 5.3` | `3.4 +/- 0.2 +4.2/-3.4` |
| Dibosons | `48 +/- 4 +/- 35` | `4.9 +/- 1.3 +/- 3.5` | `<0.5` |
| ttH | `17.7 +/- 0.4 +/- 2.4` | `18.3 +/- 0.4 +/- 2.6` | `2.6 +/- 0.2 +/- 1.9` |
| tttt | `0.59 +/- 0.04 +/- 0.39` | `1.3 +/- 0.1 +/- 1.2` | `1.0 +/- 0.1 +2.5/-1.0` |
| Other bkg | `12.3 +/- 0.5 +/- 6.4` | `7.3 +/- 0.3 +/- 4.0` | `1.1 +/- 0.2 +/- 1.1` |
| Fake/non-prompt | `170 +/- 8 +/- 87` | `53 +/- 5 +/- 28` | `7.8 +/- 1.6 +/- 3.8` |
| Charge mis-ID | `70 +/- 1 +/- 17` | `54 +/- 1 +/- 15` | `4.4 +/- 0.2 +/- 1.3` |
| Total bkg | `395 +/- 9 +/- 98` | `216 +/- 5 +/- 38` | `26 +/- 2 +/- 11` |
| Data yield | 407 | 269 | 27 |
| p-value | 0.45 | 0.10 | 0.46 |

| Source | VR1b3l | VR2b3l | VR3b3l |
| --- | ---: | ---: | ---: |
| ttW | `10.4 +/- 0.3 +/- 3.3` | `9.4 +/- 0.3 +/- 2.4` | `0.31 +/- 0.09 +0.57/-0.30` |
| ttZ | `70 +/- 1 +/- 11` | `66 +/- 1 +/- 15` | `4.6 +/- 0.2 +7.4/-4.6` |
| Dibosons | `93 +/- 7 +/- 66` | `7.7 +/- 2.1 +/- 6.2` | `0.17 +/- 0.17 +0.26/-0.00` |
| ttH | `6.5 +/- 0.2 +/- 0.8` | `6.8 +/- 0.2 +/- 0.8` | `0.41 +/- 0.05 +0.78/-0.41` |
| tttt | `0.21 +/- 0.02 +/- 0.14` | `0.64 +/- 0.03 +/- 0.37` | `0.21 +/- 0.02 +1.20/-0.21` |
| Other bkg | `27 +/- 1 +/- 14` | `12.0 +/- 0.5 +/- 6.1` | `0.7 +/- 0.2 +0.9/-0.7` |
| Fake/non-prompt | `22 +/- 4 +/- 13` | `2.7 +/- 1.5 +/- 2.1` | `0.21 +0.31/-0.18 +/- 0.12` |
| Total bkg | `229 +/- 8 +/- 70` | `105 +/- 3 +/- 19` | `6.5 +/- 0.4 +10.8/-6.5` |
| Data yield | 248 | 126 | 5 |
| p-value | 0.40 | 0.17 | 0.56 |

## Validation Region Yields: Same-Sign Top

| Source | VRtt |
| --- | ---: |
| ttW | `2.3 +/- 0.1 +/- 1.1` |
| ttZ | `1.6 +/- 0.1 +/- 0.6` |
| Dibosons | `0.5 +/- 0.4 +/- 0.3` |
| ttH | `1.0 +/- 0.1 +/- 0.4` |
| tttt | `0.30 +/- 0.03 +0.59/-0.30` |
| Other bkg | `0.7 +/- 0.1 +/- 0.6` |
| Charge mis-ID | `4.0 +/- 0.2 +/- 1.4` |
| Fake/non-prompt | `4.7 +1.5/-1.3 +/- 2.5` |
| Total bkg | `15.1 +1.6/-1.4 +/- 4.2` |
| Data yield | 22 |
| p-value | 0.14 |

## Signal Region Yields: VLQ And Four-Top

Uncertainties are statistical then systematic. The SM four-top significance row
is computed with the SM four-top yield removed from the expected background.

| Source | SR1b2l | SR2b2l | SR3b2l_L | SR3b2l |
| --- | ---: | ---: | ---: | ---: |
| ttW | `2.04 +/- 0.14 +/- 0.49` | `2.68 +/- 0.15 +/- 0.55` | `0.95 +/- 0.11 +/- 0.31` | `0.40 +/- 0.06 +/- 0.10` |
| ttZ | `0.58 +/- 0.08 +/- 0.10` | `0.95 +/- 0.11 +/- 0.17` | `0.72 +/- 0.11 +/- 0.19` | `0.11 +/- 0.05 +0.13/-0.10` |
| Dibosons | `3.2 +/- 1.5 +/- 2.4` | `<0.5` | `0.13 +/- 0.13 +0.27/-0.00` | `<0.5` |
| ttH | `0.56 +/- 0.07 +/- 0.07` | `0.57 +/- 0.10 +/- 0.09` | `0.91 +/- 0.11 +/- 0.22` | `0.19 +/- 0.05 +/- 0.07` |
| tttt | `0.10 +/- 0.01 +/- 0.05` | `0.44 +/- 0.03 +/- 0.23` | `1.46 +/- 0.05 +/- 0.74` | `0.75 +/- 0.04 +/- 0.38` |
| Other bkg | `0.52 +/- 0.07 +/- 0.14` | `0.68 +/- 0.09 +/- 0.24` | `0.47 +/- 0.08 +/- 0.18` | `0.20 +/- 0.04 +/- 0.06` |
| Fake/non-prompt | `4.1 +1.6/-1.4 +/- 2.4` | `2.5 +1.0/-0.9 +/- 1.1` | `1.2 +0.9/-0.7 +/- 0.6` | `0.20 +0.46/-0.20 +/- 0.16` |
| Charge mis-ID | `1.17 +/- 0.10 +/- 0.27` | `1.29 +/- 0.10 +/- 0.28` | `0.32 +/- 0.04 +/- 0.09` | `0.21 +/- 0.04 +/- 0.04` |
| Total bkg | `12.3 +2.2/-2.1 +/- 3.4` | `9.1 +1.2/-1.1 +/- 1.2` | `6.2 +1.0/-0.8 +/- 1.2` | `2.0 +0.5/-0.2 +/- 0.3` |
| Data yield | 14 | 10 | 12 | 4 |
| BSM significance | 0.31 | 0.25 | 1.7 | 1.1 |
| SM tttt significance | 0.33 | 0.38 | 2.1 | 1.6 |

| Source | SR1b3l | SR2b3l | SR3b3l_L | SR3b3l |
| --- | ---: | ---: | ---: | ---: |
| ttW | `0.66 +/- 0.08 +/- 0.20` | `0.38 +/- 0.05 +/- 0.11` | `0.21 +/- 0.05 +/- 0.09` | `0.15 +/- 0.04 +/- 0.05` |
| ttZ | `2.66 +/- 0.15 +/- 0.43` | `1.90 +/- 0.14 +/- 0.42` | `2.80 +/- 0.17 +/- 0.58` | `1.47 +/- 0.14 +/- 0.28` |
| Dibosons | `2.3 +/- 0.7 +/- 1.7` | `0.22 +/- 0.16 +/- 0.27` | `<0.5` | `<0.5` |
| ttH | `0.30 +/- 0.04 +/- 0.04` | `0.28 +/- 0.05 +/- 0.05` | `0.38 +/- 0.06 +/- 0.07` | `0.10 +/- 0.03 +/- 0.02` |
| tttt | `0.06 +/- 0.01 +/- 0.03` | `0.13 +/- 0.02 +/- 0.06` | `0.58 +/- 0.04 +/- 0.29` | `0.59 +/- 0.03 +/- 0.30` |
| Other bkg | `1.37 +/- 0.13 +/- 0.45` | `0.65 +/- 0.10 +/- 0.27` | `0.17 +/- 0.09 +/- 0.10` | `0.31 +/- 0.07 +/- 0.11` |
| Fake/non-prompt | `1.0 +0.6/-0.5 +/- 0.6` | `0.14 +0.31/-0.12 +/- 0.09` | `0.00 +0.38/-0.00 +0.09/-0.00` | `0.03 +0.15/-0.02 +/- 0.00` |
| Total bkg | `8.3 +0.9/-0.8 +/- 1.8` | `3.7 +0.6/-0.3 +/- 0.4` | `4.2 +0.4/-0.2 +/- 0.7` | `2.7 +/- 0.2 +/- 0.5` |
| Data yield | 8 | 4 | 9 | 3 |
| BSM significance | -0.09 | 0.14 | 1.8 | 0.19 |
| SM tttt significance | -0.07 | 0.21 | 2.1 | 0.6 |

## Signal Region Yields: Same-Sign Top

| Source | SRttee | SRttemu | SRttmumu |
| --- | ---: | ---: | ---: |
| ttW | `0.91 +/- 0.09 +/- 0.19` | `2.64 +/- 0.15 +/- 0.48` | `1.86 +/- 0.13 +/- 0.37` |
| ttZ | `0.35 +/- 0.07 +/- 0.09` | `0.91 +/- 0.09 +/- 0.12` | `0.47 +/- 0.08 +/- 0.09` |
| Dibosons | `0.40 +/- 0.45 +/- 0.09` | `1.4 +/- 0.6 +/- 0.9` | `0.5 +/- 0.5 +/- 0.5` |
| ttH | `0.19 +/- 0.06 +/- 0.02` | `0.53 +/- 0.08 +/- 0.08` | `0.58 +/- 0.07 +/- 0.05` |
| tttt | `0.12 +/- 0.02 +/- 0.06` | `0.30 +/- 0.02 +/- 0.15` | `0.22 +/- 0.03 +/- 0.11` |
| Other bkg | `0.29 +/- 0.06 +/- 0.13` | `0.51 +/- 0.08 +/- 0.16` | `0.33 +/- 0.08 +/- 0.12` |
| Fake/non-prompt | `3.4 +2.1/-1.7 +/- 2.5` | `3.3 +1.2/-1.1 +/- 2.1` | `0.20 +0.24/-0.20 +/- 0.18` |
| Charge mis-ID | `1.90 +/- 0.11 +/- 0.91` | `2.69 +/- 0.14 +/- 0.59` | N/A |
| Total bkg | `7.5 +2.2/-1.8 +/- 2.7` | `12.2 +/- 1.3 +/- 2.5` | `4.2 +0.6/-0.6 +/- 0.7` |
| Data yield | 9 | 13 | 8 |
| Significance | 0.31 | 0.16 | 1.44 |

## Systematic Uncertainty Summary

Total-background uncertainty percentages for VLQ/four-top signal regions:

| Source | SR1b2l | SR2b2l | SR3b2l_L | SR3b2l | SR1b3l | SR2b3l | SR3b3l_L | SR3b3l |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Jet energy resolution | 3 | 1 | 5 | 6 | 3 | 5 | 3 | 4 |
| Jet energy scale | 3 | 3 | 9 | 6 | 3 | 5 | 11 | 6 |
| b-tagging efficiency | 5 | 3 | 6 | 7 | 3 | 4 | 9 | 9 |
| Lepton ID efficiency | 2 | 1 | 1 | 1 | 3 | 3 | 2 | 3 |
| Pile-up reweighting | 5 | 2 | 3 | 3 | 3 | 5 | 1 | 6 |
| Luminosity | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 2 |
| Fake/non-prompt | 20 | 12 | 13 | 8 | 7 | 2 | 3 | 1 |
| Charge mis-ID | 2 | 3 | 1 | 2 | - | - | - | - |
| Cross-section x acceptance | 25 | 13 | 22 | 32 | 32 | 26 | 21 | 24 |

Representative VLQ `T` signal expected yields and experimental uncertainty
percentages, for `mT = 1 TeV`:

| Source | SR1b2l | SR2b2l | SR3b2l_L | SR3b2l | SR1b3l | SR2b3l | SR3b3l_L | SR3b3l |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Jet energy resolution | <1 | 1 | 6 | 4 | <1 | <1 | 24 | <1 |
| Jet energy scale | 2 | 1 | 23 | 3 | 1 | 1 | 12 | <1 |
| b-tagging efficiency | 6 | 3 | 9 | 8 | 5 | 4 | 7 | 8 |
| Lepton ID efficiency | 2 | 2 | 1 | 2 | 3 | 3 | 2 | 3 |
| Luminosity | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| Pile-up reweighting | 3 | 3 | 7 | 3 | <1 | <1 | 3 | 2 |
| Expected yield | 1.7 | 2.1 | 0.08 | 1.0 | 3.0 | 3.2 | 0.03 | 1.8 |

Total-background uncertainty percentages for same-sign top signal regions:

| Source | SRttee | SRttemu | SRttmumu |
| --- | ---: | ---: | ---: |
| Jet energy resolution | 3 | <1 | 13 |
| Jet energy scale | 2 | 2 | 9 |
| b-tagging efficiency | 1 | 2 | 3 |
| Lepton ID efficiency | <1 | 1 | 4 |
| Pile-up reweighting | 2 | 2 | 4 |
| Luminosity | <1 | 1 | 2 |
| Fake/non-prompt | 36 | 17 | 5 |
| Charge mis-ID | 12 | 5 | - |
| Cross-section x acceptance | 10 | 15 | 25 |

Representative same-sign-top signal expected yields and experimental uncertainty
percentages, for exclusive `tt` production with `mV = 2 TeV`, normalized to
100 fb:

| Source | SRttee | SRttemu | SRttmumu |
| --- | ---: | ---: | ---: |
| Jet energy resolution | 7 | <1 | <1 |
| Jet energy scale | 1 | 1 | <1 |
| b-tagging efficiency | 3 | 2 | <1 |
| Lepton ID efficiency | 5 | 3 | 4 |
| Luminosity | 2 | 2 | 2 |
| Pile-up reweighting | 3 | <1 | 1 |
| Expected yield | 3.4 | 13 | 12 |

## Headline Limits And Outcomes

Global outcome:

- No statistically significant excess over expected background.
- Notable counting excesses: `SR3b2l_L` at 1.7 sigma and `SR3b3l_L` at
  1.8 sigma.
- SM four-top observed significance: 3.0 sigma; expected: 0.9 sigma.
- Largest BSM model significance: 2.3 sigma for the 2HDM interpretation.

VLQ limits:

| Result | Observed | Expected |
| --- | ---: | ---: |
| Vector-like B singlet lower mass limit | 1.00 TeV | 1.01 TeV |
| Vector-like T singlet lower mass limit | 0.98 TeV | 0.99 TeV |
| Vector-like T5/3 pair-production lower mass limit | 1.19 TeV | 1.21 TeV |
| Vector-like T5/3 pair plus single production lower mass limit, coupling = 1.0 | 1.6 TeV | 1.7 TeV |

Four-top limits:

| Observable | Expected median | Expected 1 sigma range | Observed |
| --- | ---: | ---: | ---: |
| SM four-top cross-section upper limit | 29.0 fb | `+12.2 / -8.1` fb | 69.2 fb |
| CI four-top cross-section upper limit | 20.8 fb | `+12.2 / -8.1` fb | 38.6 fb |
| CI coupling `abs(C4t) / Lambda^2` upper limit | 1.9 TeV^-2 | `+1.2 / -0.7` TeV^-2 | 2.6 TeV^-2 |
| 2UED/RPP `mKK` lower limit | 1.48 TeV | not tabulated | 1.45 TeV |

Same-sign top / FCNC dark-matter mediator limits:

| Result | Observed | Expected |
| --- | ---: | ---: |
| Generic `u u -> t t`, `mV = 1 TeV`, cross-section upper limit | 89 fb | 59 fb |
| `gSM` upper limit for `mV = 3 TeV`, `gDM = 1` | 0.31 | 0.28 |
| `gSM` upper limit for `mV = 1 TeV`, `gDM = 1` | 0.14 | 0.13 |

Figures provide additional cross-section-limit curves and exclusion contours for
VLQ branching-ratio scans, T5/3 mass/coupling planes, 2UED/RPP, 2HDM, and
same-sign-top mediator parameter planes. The paper text and extracted tables do
not provide all numeric curve points.
