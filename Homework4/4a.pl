/* 4. a. */



follows([M1,M2,M3,C1,C2,X],[M1,M2,M3,C1,C2,Y]) :- change(X,Y).
follows([M1,M2,M3,C1,X,C3],[M1,M2,M3,C1,Y,C3]) :- change(X,Y).
follows([M1,M2,M3,X,C2,C3],[M1,M2,M3,Y,C2,C3]) :- change(X,Y).
follows([M1,M2,X,C1,C2,C3],[M1,M2,Y,C1,C2,C3]) :- change(X,Y).
follows([M1,X,M3,C1,C2,C3],[M1,Y,M3,C1,C2,C3]) :- change(X,Y).
follows([X,M2,M3,C1,C2,C3],[Y,M2,M3,C1,C2,C3]) :- change(X,Y).
follows([M1,M2,M3,C1,X,X],[M1,M2,M3,C1,Y,Y]) :- change(X,Y).
follows([M1,M2,M3,X,C2,X],[M1,M2,M3,Y,C2,Y]) :- change(X,Y).
follows([M1,M2,X,C1,C2,X],[M1,M2,Y,C1,C2,Y]) :- change(X,Y).
follows([M1,X,M3,C1,C2,X],[M1,Y,M3,C1,C2,Y]) :- change(X,Y).
follows([X,M2,M3,C1,C2,X],[Y,M2,M3,C1,C2,Y]) :- change(X,Y).
follows([M1,M2,M3,X,X,C3],[M1,M2,M3,Y,Y,C3]) :- change(X,Y).
follows([M1,M2,X,C1,X,C3],[M1,M2,Y,C1,Y,C3]) :- change(X,Y).
follows([M1,X,M3,C1,X,C3],[M1,Y,M3,C1,Y,C3]) :- change(X,Y).
follows([X,M2,M3,C1,X,C3],[Y,M2,M3,C1,Y,C3]) :- change(X,Y).
follows([M1,M2,X,X,C2,C3],[M1,M2,Y,Y,C2,C3]) :- change(X,Y).
follows([M1,X,M3,X,C2,C3],[M1,Y,M3,Y,C2,C3]) :- change(X,Y).
follows([X,M2,M3,X,C2,C3],[Y,M2,M3,Y,C2,C3]) :- change(X,Y).
follows([M1,X,X,C1,C2,C3],[M1,Y,Y,C1,C2,C3]) :- change(X,Y).
follows([X,M2,X,C1,C2,C3],[Y,M2,Y,C1,C2,C3]) :- change(X,Y).
follows([X,X,M3,C1,C2,C3],[Y,Y,M3,C1,C2,C3]) :- change(X,Y).

change(e,w).
change(w,e).

admissible([w,w,w,X,Y,Z]).
admissible([e,e,e,X,Y,Z]).

admissible([M7,M8,M9,C7,C8,C9]) :-
	w_count([M7,M8,M9], MW),
	w_count([C7,C8,C9], CW),
	MW == CW.

w_count([e,e,e], 0).
w_count([w,A,B], D) :-
	w_count([e,A,B], F),
	D = F+1.
w_count([A,w,B], D) :-
	w_count([A,e,B], F),
	D = F+1.
w_count([A,B,w], D) :-
	w_count([A,B,e], F),
	D = F+1.

plan(Goal, Goal, List) :- write(List).
plan(State, Goal, List) :-
	admissible(NextState),
	follows(NextState,State),
	not(member(NextState,List)),
	plan(NextState,Goal,[NextState|List]).
	

/*
car([X|Y],X).

plan([],[e,e,e,e,e,e],[[e,e,e,e,e,e]]).

plan(X,Goal,[State|L]) :-
	write("True\n"),
	car(X,T),
	car(L,U),
	follows(T,U),
	admissible(State),
	not(member(State,L)), 
	plan([State|X],Goal,L).
	
plan(X,Goal,[State|L]) :-
	write("False\n"),
	car(X,T),
	car(L,U),
	follows(T,U),
	admissible(State),
	not(member(State,L)), 
	plan([],Goal,L).
*/
