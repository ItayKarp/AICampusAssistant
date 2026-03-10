# Red-team rerun summary

Same suite rerun against the uploaded codebase.

- Previous result: 5 passed / 8 failed
- Current result: 7 passed / 6 failed

## Fixed on rerun
- T02 `class_code` contract works
- T06 `day_of_week` contract works
- T10 classifier exception is sanitized
- T11 responder crash no longer returns HTTP 500
- T13 classifier instruction file format is cleaned up

## Still failing
- T01 course lookup by `course_name`
- T04 exam lookup by `course_name`
- T05 legacy `day` key no longer works
- T07 invalid legacy `day` key is not rejected
- T08 unsupported classifier categories still fall through
- T12 "my" exam query is still not isolated in the same test

## Highest-priority remaining fixes
1. Add `course_name` handling in exam repo, or stop the classifier from ever emitting it for exam filtering.
2. Return an explicit unsupported-category error instead of `{}`.
3. Make self-scoped queries enforce user scoping end-to-end.
4. Decide whether `day` remains a backwards-compatible alias. If not, update tests and contract docs together.
5. Accept `course_name` as an alias in course repo, or make the contract consistently use `class_name`.
