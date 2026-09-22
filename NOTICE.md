# Notice

**Scope of this repository.** It publishes *documentation* and *synthetic sample outputs* of five
tools, for evaluation by a prospective client. It does not publish source code.

**Data.** Every published output is generated from synthetic fixtures. No client data, client
identity, client location, engagement terms or pricing appears in this repository. The publication
step is scripted and its logic is public: [`tools/build_showcase.py`](tools/build_showcase.py)
replaces blocklisted strings and then re-reads the result, refusing to publish any file where a
string survives. The policy file that feeds it is kept outside this repository, because the
blocklist itself names the clients it protects.

**Rights.** The documentation, the sample outputs and the artwork in this repository are published
for reading and evaluation only. No licence is granted to copy, redistribute, resell, sublicense or
incorporate them into another product or service. The tools themselves are delivered under the
terms of the corresponding engagement.

**Trademarks.** Third-party names appear only to identify the systems the tools integrate with
(Excel, Google Sheets, Xero, Walmart, Xero is a trademark of Xero Limited). Their use is descriptive
and implies no affiliation or endorsement.

**No warranty.** Sample outputs are illustrations, not advice. The analytical figures shown are
computed from synthetic data and mean nothing about any real business.

**Contact.** [josedrobles.com](https://josedrobles.com)
