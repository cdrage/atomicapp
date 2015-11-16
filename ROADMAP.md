# Atomic App Roadmap

This document provides a roadmap for current Atomic App development. The dates and features listed below are not considered final but rather an indication of what the core contributors are working on and the direction of Atomic App.

Atomic App is the implementation of the [Nulecule spec](https://github.com/projectatomic/nulecule). We follow the spec closely, the current spec version as well as Atomic App version can be found via `atomicapp --version`.

__Unless otherwise announced, the Atomic App CLI as well as Nulecule spec are subject to change. Backwards compatibility is a priority for version _1.0.0_. __ 


#### Atomic App 0.3.0 (Early Dec?)
 - Refactor logging [#134](https://github.com/projectatomic/atomicapp/issues/134)
 - Mesos provider [#357](https://github.com/projectatomic/atomicapp/issues/357)
 - Fix ordering arguments of CLI [#332](https://github.com/projectatomic/atomicapp/issues/332)

#### Atomic App 0.4.0 (Late Dec?)
 - Keep versioning info in one location [#155](https://github.com/projectatomic/atomicapp/issues/155)
 - Implement stop for OpenShift provider [#135](https://github.com/projectatomic/atomicapp/issues/135)
 - Refactoring OpenShift provider [#321](https://github.com/projectatomic/atomicapp/issues/321)

#### Atomic App 1.0.0

 - Docker compose provider [#265](https://github.com/projectatomic/atomicapp/issues/265)
 - Ansible provider [#170](https://github.com/projectatomic/atomicapp/issues/170)
 - Nspawn provider [#262](https://github.com/projectatomic/atomicapp/issues/262)
 - Add a `USER` to Atomic App image [#252](https://github.com/projectatomic/atomicapp/issues/252)
 - https/ssh/sftp support for artifacts
 - Support running Kubernetes from an Openshift template [#131](https://github.com/projectatomic/atomicapp/issues/131)
 - Persistent storage
