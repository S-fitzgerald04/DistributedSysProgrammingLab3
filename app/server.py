import l o g gi n g
2 import time
3 from c o n c u r r e n t import f u t u r e s
4
5 import g rpc
6
7 from app . gameimpl import x01_match
8 from darts_match_pb2 import Vi si tR e s p o n s e , Re gi s te rRe sp on se ,
Fi n ali z eR e s p o n s e , MatchResponse , \
9 WatchResponse , Player , Dart
10 from darts_match_pb2_grpc import D a r t sM a tchSe rvice r ,
add_DartsMatchServicer_to_server
11 from app . s e r v e r . m a tch_ re gi s t r y import MatchRegistry
12 from domain import darts_match , v i s i t
13 from p a t t e r n import o b j e c t_ f a c t o r y
14
15
16 c l a s s D a r tSe r ve r ( D a r t sM a tchSe r vice r ) :
17
18 d e f __init__ ( s e l f ) :
19 # temp / t e s t v al u e s f o r j u s t 1 match i n i t i a l l y
20 s e l f . match_type = "X01"
21 s e l f . f a c t o r y = o b j e c t_ f a c t o r y . Ob jec tF ac t o ry ( )
6
22 s e l f . f a c t o r y . r e g i s t e r _ b u i l d e r ( 'X01 ' , x01_match . X01MatchBuilder ( ) )
23 s e l f . r e g i s t r y = MatchRegistry . g e t_i n s t a n c e ( )
24
25 d e f P r o c e s s V i s i t ( s e l f , r e q u e s t , c o n t e x t ) :
26 p r i n t ( " i n ' v i s i t ' f o r : " + s t r ( r e q u e s t . matchId ) )
27 my_visit = v i s i t . V i s i t ( r e q u e s t . v i s i t )
28 match = s e l f . r e g i s t r y . get_match ( r e q u e s t . matchId )
29 r e s u l t , r e s p o n s e = match . p r o c e s s _ v i s i t ( r e q u e s t . pl a y e r I n d e x ,
my_visit )
30 r e t u r n Vi si tR e s p o n s e ( r e s u l t=r e s u l t , message=r e s p o n s e )
31
32 d e f R e gi s t e rPl a y e r ( s e l f , r e q u e s t , c o n t e x t ) :
33 p r i n t ( " i n r e g i s t e r pl a y e r " )
34 match = s e l f . r e g i s t r y . get_match ( r e q u e s t . matchId )
35 pl aye r_index = match . match . r e g i s t e r _ p l a y e r ( r e q u e s t . userName )
36 p r i n t ( match . match . pl a y e r s )
37 r e t u r n R e gi s t e rR e s p o n s e ( pl a y e r I n d e x=pl aye r_index )
38
39 d e f Fi n ali z eM a t c h ( s e l f , r e q u e s t , c o n t e x t ) :
40 p r i n t ( " i n f i n a l i z e " )
41 s e l f . r e g i s t r y . get_match ( r e q u e s t . matchId ) . f i n a l i z e _ s e t u p ( )
42 r e t u r n Fi n ali z e R e s p o n s e ( )
43
44 d e f CreateMatch ( s e l f , r e q u e s t , c o n t e x t ) :
45 """
46 This i s s t a t e l e s s , i . e . no d e di c a t e d s e s s i o n f o r the match ; must
r e t u r n the unique i d o f the match and t h i s
47 must be s e n t a s a parameter with a l l r e q u e s t s . Like s e s s i o n s on a
multi−th re aded web se r ve r .
48 : param r e q u e s t :
49 : param c o n t e x t :
50 : r e t u r n : match_id
51 """
52 p r i n t ( " i n c r e a t e match" )
53 new_match = s e l f . f a c t o r y . c r e a t e ( r e q u e s t . matchType )
54 match = darts_match . DartsMatch ( )
55 match . r e g i s t e r _ p l a y e r ( r e q u e s t . userName )
56 new_match . set_match ( match )
57 match_id = s e l f . r e g i s t r y . add_match ( new_match )
58 p r i n t ( "Created match : " + s t r ( match_id . b y t e s ) )
59 r e t u r n MatchResponse ( matchId=match_id . b y t e s )
60
61 d e f WatchMatch ( s e l f , r e q u e s t , c o n t e x t ) :
62 # g e t through any ol d e r v i s i t s
63 my_uuid = l i s t ( MatchRegistry . g e t_i n s t a n c e ( ) . matches . key s ( ) ) [ 0 ] .
b y t e s # temporary − j u s t g e t f i r s t uuid
64 # match = s e l f . r e g i s t r y . get_match ( r e q u e s t . matchId )
65 match = s e l f . r e g i s t r y . get_match (my_uuid )
66
67 v = 0
68 f o r v i n r an ge ( 0 , l e n ( match . match . v i s i t s [ 0 ] ) ) :
69 f o r p i n r an ge ( 0 , l e n ( match . match . pl a y e r s ) ) :
70 w hil e l e n ( match . match . v i s i t s [ p ] ) < l e n ( match . match . v i s i t s
[ 0 ] ) :
7
71 # we may need t o w ai t f o r the next pl a y e r t o c a tch up
on v i s i t s
72 time . s l e e p ( 1 )
73 my_visit = match . match . v i s i t s [ p ] [ v ]
74 y i e l d WatchResponse ( pl a y e r=Pl a ye r ( userName=match . match .
pl a y e r s [ p ] , pl a y e r I n d e x=p ) ,
75 d a r t s =[Dart ( m u l t i p l i e r=my_visit . d a r t s
[ 0 ] . m u l t i p l i e r ,
76 segment=my_visit . d a r t s [ 0 ] .
segment ) ,
77 Dart ( m u l t i p l i e r=my_visit . d a r t s
[ 1 ] . m u l t i p l i e r ,
78 segment=my_visit . d a r t s [ 1 ] .
segment ) ,
79 Dart ( m u l t i p l i e r=my_visit . d a r t s
[ 2 ] . m u l t i p l i e r ,
80 segment=my_visit . d a r t s [ 2 ] .
segment ) ] ,
81 s c o r e =0) # I t would be ni c e t o p r o vi d e
more than j u s t the d a r t s thrown
82
83 # Now s t a r t watching new v i s i t s
84 w hil e True :
85 i f l e n ( match . match . v i s i t s [ 0 ] ) > v + 1 :
86 y = l e n ( match . match . v i s i t s [ 0 ] )
87 f o r x i n r an ge ( v + 1 , y ) :
88 f o r p i n r an ge ( 0 , l e n ( match . match . pl a y e r s ) ) :
89 w hil e l e n ( match . match . v i s i t s [ p ] ) < y :
90 # we may need t o w ai t f o r the next pl a y e r t o
c a t ch up on v i s i t s
91 time . s l e e p ( 1 )
92 y i e l d WatchResponse ( pl a y e r=Pl a ye r ( userName=match .
match . p l a y e r s [ p ] , pl a y e r I n d e x=p ) ,
93 d a r t s =[Dart ( m u l t i p l i e r=match .
match . v i s i t s [ p ] [ x ] . d a r t s [ 0 ] . m u l t i p l i e r ,
94 segment=match . match
. v i s i t s [ p ] [ x ] . d a r t s [ 0 ] . segment ) ,
95 Dart ( m u l t i p l i e r=match .
match . v i s i t s [ p ] [ x ] . d a r t s [ 1 ] . m u l t i p l i e r ,
96 segment=match . match
. v i s i t s [ p ] [ x ] . d a r t s [ 1 ] . segment ) ,
97 Dart ( m u l t i p l i e r=match .
match . v i s i t s [ p ] [ x ] . d a r t s [ 2 ] . m u l t i p l i e r ,
98 segment=match . match
. v i s i t s [ p ] [ x ] . d a r t s [ 2 ] . segment ) ] ,
99 s c o r e =0)
100 v = y − 1
101 time . s l e e p ( 1 )
102
103
104 d e f s e r v e ( ) :
105 s e r v e r = g rpc . s e r v e r ( f u t u r e s . ThreadPoolExecutor ( max_workers=10) )
106 add_DartsMatchServicer_to_server ( D a r tSe r ve r ( ) , s e r v e r )
107 s e r v e r . add_insecure_port ( ' [ : : ] : 5 0 0 5 5 ' )
8
108 s e r v e r . s t a r t ( )
109 s e r v e r . w ai t_ f o r_ te rmin a ti on ( )
110
111
112 i f __name__ == '__main__ ' :
113 l o g gi n g . b a si c C o n fi g ( )
114 s e r v e (
