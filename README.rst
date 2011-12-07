####################
Circular role dealer
####################

Story
=====

This application has been created to distribute roles in a game, with the
following rules:

* there are two roles: giver and receiver;
* a "giver" gives something to a "receiver";
* everybody is "giver" once, and only once;
* everybody is "receiver" once, and only once;
* players are grouped in teams of one or two persons;
* a player is member of one and only one team;
* members of a team cannot give to or receive from other members in the same
  team;
* roles are randomly distributed;
* the schema of all giver-receiver connections makes one big ring which
  includes all participants. It means that there cannot be two rings, only one.

Optionally, if we distribute roles several times:

* a player cannot give twice to the same person (change distribution)
* a player cannot give to someone who was his former giver (no "revenge")
* with respect to at least one level in history

Which game?
===========

The first use-case was the following:

* friends or family are invited to a party
* everybody has to bring a small gift dedicated to someone else
  (giver/receiver)
* nobody knows who will give him/her a present (surprise!)
* teams are made of couples (you don't give something to your wife/husband/...)

... but there may be other use-cases!

Example
=======

Here is the family of Peter and Paula, they have 3 sons called Patrick, Mark
and Steve. Patrick lives with Joe. Mark is single. Steve lives with Sandra.
Here are the teams:

* Peter, Paula
* Patrick, Joe
* Mark
* Steve, Sandra

After the random distribution, we can obtain the following ring:

* Peter   gives to Joe
* Joe     gives to Sandra
* Sandra  gives to Mark
* Mark    gives to Paula
* Paula   gives to Steve
* Steve   gives to Patrick
* Patrick gives to Peter

It can be displayed as a list: Peter, Joe, Sandra, Mark, Paula, Steve,
Patrick... and Peter again.

Of course, you can use this utility with friends!

Known issues
============

* Not accurate with very small amount of players or teams.
* Teams of more than 2 players are not supported.
* The implementation doesn't cover all permutations.

Usage
=====

.. note::

  If you just want to try this application, you can:

  * follow the testing procedure to install a copy of this project;
  * run "bin/bpython" in a shell;
  * then type the following commands in the bpython shell.

::

  from marmelune.games.circularroledealer.dealer import CircularDealer

  players = [['Andrew'],
             ['Balthazar', 'Beyonce'],
             ['Clothilde', 'Cassius'],
             ['Dan'],
             ['Eleanor', 'Esmeralda'],
             ['Frida', 'Frank'],
            ]
  dealer = CircularDealer(players)
  dealer.deal()
  dealer.deal()
  dealer.deal()
  dealer.history

Another sample script that you can run with bin/python sample.py

::

  # Save this as sample.py
  from marmelune.games.circularroledealer import dealer


  players = [['Pedro', 'Simone'],
             ['Louis', 'Paulette'],
             ['Marcel', 'Chuck'],
             ['Regine', 'Paul'],
             ['Sullivan', 'Clara'],
             ['Maria', 'Thomas'],
            ]

  d = dealer.CircularDealer(players)

  # 1st round.
  d.history.append(['Simone', 'Paulette', 'Paul', 'Sullivan', 'Maria',
                    'Chuck', 'Pedro', 'Regine', 'Louis', 'Marcel', 'Clara'])
  # 2nd round.
  d.history.append(['Simone', 'Sullivan', 'Paulette', 'Regine', 'Marcel',
                    'Maria', 'Pedro', 'Clara', 'Chuck', 'Paul', 'Louis'])
  # 3rd round. Notice that Thomas was not present in previous rounds.
  d.history.append(['Clara', 'Regine', 'Maria', 'Simone', 'Chuck', 'Louis',
                    'Sullivan', 'Pedro', 'Paulette', 'Thomas', 'Marcel',
                    'Paul'])
  # Next!
  print d.deal_with_respect_to_history()


Testing
=======

.. sourcecode:: sh

  # Download project
  git clone https://github.com/Sullivanbryon/marmelune.games.circularroledealer
  cd marmelune.games.circularroledealer
  # Bootstrap
  bin/bootstrap
  # Deploy
  bin/buildout -N
  # Run tests
  bin/nosetests --with-doctest --rednose src/marmelune/games/circularroledealer/
