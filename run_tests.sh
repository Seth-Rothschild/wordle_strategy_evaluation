#!/bin/bash

black .
flake8
pytest
