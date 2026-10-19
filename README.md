
# INDANGA: early warning for every child

Student prototype for the **UNICEF Rwanda @40 Pan-African Student Competition** (Kigali, 30 October 2026).

INDANGA (from the Kinyarwanda *kuranga*, to flag) links the school, health, immunisation and social
protection data Rwanda already collects into one transparent risk score per child, and tells frontline
workers which child to visit, why, and which service to call. A person reviews every alert.

**All data in this app is simulated. No real child is represented.**

## What the demo shows
1. **District overview**: risk by sector, what drives the alerts, a fairness check, and an under five
   nutrition and immunisation watch.
2. **Children to visit**: a priority list with reasons and suggested actions, exportable as CSV.
3. **Child profile and what if**: explainable risk, live "what if" sliders, and the SMS a frontline
   worker would receive.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Author
Tchandikou Ouadja Fare, African Institute for Mathematical Sciences (AIMS) Rwanda.

Photo © UNICEF/UNI725007/Iyakaremye, used with credit for this competition entry.
This is an independent student prototype, not an official UNICEF product.

# indanga-demo
