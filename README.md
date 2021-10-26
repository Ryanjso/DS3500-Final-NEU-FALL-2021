# Project Proposal

### Motivation 

Poker is an extremely complicated game, and it is often described as one of the only games at a casino that is a game of skill. In poker there is never a right move to be made. You can have the worst cards and still win, or even lose while holding the best cards. This complexity makes the task of creating a poker AI very challenging, and worthy of a semester long project. If done properly this project will demonstrate advanced knowledge and experience in multiple fields of computer science. These fields include machine learning, advanced usage of algorithms, object oriented programming, and web development. 

### Goals and Objectives  

We hope to create an AI powerful enough to beat a professional poker player. Our code will be able to create and manage a game of No Limit Texas Hold ‘em. We will utilize a concept known as counterfactual regret minimization (CRF) to train our AI. The idea behind CRF is that each time our AI completes a game of poker, it revisits all of its decisions and calculates a level of regret for making, or not making each choice. Our AI will then use these calculated regret scores to make more informed decisions in the future. Our AI will play against itself several thousand times an hour to improve its poker skill. One major component of poker is bluffing, which is essentially trying to make other player(s) on the table make certain decisions by betting notable amounts. We consider bluffing to be one of the most human-like parts of the game as it relies heavily on taking advantage of human psychology. We are curious to see how our AI reacts to bluffing, and if it will develop its own strategy of bluffing. 


### Data Sources 

Our project will utilize counterfactual regret minimization to improve performance. Effectively, it will play against itself over millions of games instead of using training and test data. One possible limitation is the amount of compute-power required for the algorithm to simulate millions or even billions of poker games, and calculate regret scores. Because CRF appears to be similar to evolutionary computing in the sense that millions of generated candidate strategies are evaluated to reach an optimal solution, we anticipate that Professor Rachlin may be able to advise us on how to overcome this challenge.
Texas Hold’em Rules: https://www.pokernews.com/poker-rules/texas-holdem.htm

### Platform Architecture

This project will use Object Oriented Programming in order to build out the functionality for creating users, cards, game decks, players, and poker tables, and a Poker AI. In addition, we will connect this with a React/Javascript frontend in order for the user to interact with the previously mentioned functionality. We hope to create a platform where a player can play 1 vs 1 Texas Hold Em Poker with the AI that we develop.
