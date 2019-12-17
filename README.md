# Flagit

> This is a restful API which receives a set of sentences and it returns 'true' or 'false' depending if it matches the criteria.

![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)

**Usage**

- Send a `POST` request containing a `JSON` structure as below

```buildoutcfg
{
    "task": "flag_it",
    "sentences" : [
                    "This is one sentence",
                    "This is another one"
                  ]
}
```
- The results will be received as

```buildoutcfg
{
    "task": "flag_it",
    "sentences" : [
                    ["This is one sentence", false],
                    ["This is another one", true]
                  ]
}
```
