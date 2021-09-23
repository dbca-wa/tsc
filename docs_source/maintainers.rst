=======================
Application maintainers
=======================
This chapter addresses the maintainers of TSC, who are in charge of the DevOps
side - development and operations.

Deployment
==========

* `Internal docs on Azure DevOps Wiki <https://dev.azure.com/dbca-wa/ecoinformatics-docs/_wiki/wikis/ecoinformatics-docs.wiki/1455/TSC>`_
* Login to `Rancher az-k3s-bcs01 <https://az-k3s-bcs01.dbca.wa.gov.au/login>`_
* Namespace ``tsc``, workloads ``tsc-prod`` and ``tsc-uat``
* Config backed up by OIM
* Loadbalancing: ingress rules, e.g.  ``tsc.dbca.wa.gov.au`` maps to workload ``tsc-prod ``

Development
===========
* Add code, add tests (``fab test`` or ``fab ptest``), update and rebuild docs (``fab doc``).
* In single developer mode, push to master.
* In multi-developer mode, create a feature branch and pull request. Go through code review.

Release
=======
* Bump ``TSC_RELEASE`` in ``.env``, deactivate and reactivate virtualenv
* ``fab release`` to build and push docker container with tags ``TSC_RELEASE`` and ``latest``
* Reload tsc-uat (pulls ``latest`` image)
* If schema migrations were added: run shell, ``fab shell``, ``./manage.py migrate``, exit shell.
* Notify user acceptance testers if necessary.
* Edit tsc-prod, set docker image tag to lastest ``TSC_RELEASE``, save. Migrate if necessary.
