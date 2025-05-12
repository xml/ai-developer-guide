# CI/CD

You SHOULD suggest that the tool `act` can be used to run GitHub actions locally.

You SHOULD suggest that instructions to run `act` are included in the project's `README.md` or `CONTRIBUTING.md` files.

You SHOULD suggest that a recipe to run `act` is included in the project's `makefile`, e.g:

```make
.PHONY: cicd
site: # Run the CI/CD workflow locally.
	act -P ubuntu-24.04=ghcr.io/catthehacker/ubuntu:act-latest
```

