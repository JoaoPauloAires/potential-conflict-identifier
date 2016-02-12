This README tries to explain how to execute the contract_data_structure.py.

=======================================================================
Execute:
=======================================================================

- To execute run the following command:
	python -B contract_data_structure.py

=======================================================================
Options:
=======================================================================

- After the identification step, there will be two initial options:
	(1) Pick a random contract; and
	(4) Finish.

(1) This option chooses, at random, a contract from the corpus.
	It may return an error, but that is OK, press (1) again.
	If it does not return an error, it will present a series of information,
	such as the total number of norms extracted and the parties identified;

(4)	This option just clear the folder and exit.

- When a contract is chosen, an option is added:

	(1) Pick up a random contract; 
	(2) Pick up a random norm; and
	(4) Finish. 

(1) Restart the process with a new contract;

(2) Choose a random norm among the extracted ones.

- When a norm is chosen, an option is added:

	(1) Pick up a random contract; 
	(2) Pick up a random norm;
	(3) Make a conflict; and
	(4) Finish. 

(1)(2)(4) Same as before;

(3) This option displays the last chosen norm and asks you to alter in order
	to create a conflict.

=======================================================================
Process:
=======================================================================

- In this manual conflict insertion you are intended to follow a series of
  steps.
  First, you have to execute, insert your first name, and pick up a contract (1).
  Then, you have to choose a random norm.

- You have to create between 70 and 100 conflicts within 3 types.
These types are:
	- Permission x Obligation  (33%)
	- Permission x Prohibition (33%)
	- Obligation x Prohibition (33%)

- A regular norm, which you will have to consider in order to alter, has the 
following structure:

	Example 1. "Purchaser must pay the product taxes."

 In the example, "Purchaser" is one of the parties, it MUST appear BEFORE the
 modal verb.
 If there is no party before the modal verb, get another norm (option 2).
 You can also get another contract (option 1).

- Given a regular norm, you will choose option 3, which allows you to alter such
  norm.
  Then you have to alter it in order to generate a conflict, e.g., if you got the
  Example 1, you may choose to create either a Permission x Obligation conflict or
  an Obligation x Prohibition conflict.
  In the first case (Permission x Obligation), a possible modification can be described
  as follows:

  	Example 2. "Purchaser MAY pay the product taxes."

  To ensure that you are really making a conflict, use the Table below as a guide:
  -------------------------------------
  | Modal Verb 		| Deontic Meaning |
  -------------------------------------
  | can 	  		| Permission      |
  | may        		| Permission      |
  | must       		| Obligation      |
  | ought      		| Obligation      |
  | shall      		| Obligation      |
  | will	   		| Obligation      |
  | modal_verb not  | Prohibition     |

  You may also modify the structure after the modal verb creating a conflict and altering
  the conflict structure (obviously maintaining the same meaning), as the Example 3 shows.

  	Example 3. "Purchaser may choose to pay the taxes related to the product."

- We recommend you to use more than three contracts to create conflicts, it allows us to
  test our approach in different contexts.

- At the end of the process, choose option (4) and that's it!

Thanks in advance.