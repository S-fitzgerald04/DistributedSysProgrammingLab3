import t h r e a di n g
2 import uuid
3
4
5 c l a s s MatchRegistry :
6 """ Simple in−memory implemen t a ti on f o r now ; thread−s a f e
7
8 """
9 __instance = None
10
11 d e f __init__ ( s e l f ) :
12 i f MatchRegistry . __instance i s not None :
13 r a i s e Excep ti on ( "This i s a s i n g l e t o n ! " )
14 e l s e :
15 MatchRegistry . __instance = s e l f
16 s e l f . l o c k = t h r e a di n g . Lock ( )
17 s e l f . matches = {}
18 s e l f . i n s t a n c e = None
19
2
20 @staticmethod
21 d e f g e t_i n s t a n c e ( ) :
22 i f MatchRegistry . __instance i s None :
23 with t h r e a di n g . Lock ( ) :
24 i f MatchRegistry . __instance i s None : # Double l o c k i n g
mechanism
25 MatchRegistry ( )
26 r e t u r n MatchRegistry . __instance
27
28 d e f add_match ( s e l f , match ) :
29 s e l f . l o c k . a c q ui r e ( )
30 match_id = uuid . uuid4 ( ) # g e n e r a t e what w i l l alm o s t c e r t a i n l y be a
unique i d (may need t o i n v e s t i g a t e SafeUUID)
31 s e l f . matches [ match_id ] = match
32 s e l f . l o c k . r e l e a s e ( )
33 r e t u r n match_id
34
35 d e f get_match ( s e l f , match_id ) :
36 r e t u r n s e l f . matches [ uuid .UUID( b y t e s=match_id ) ]
