import l o g gi n g
2
3 import g rpc
4
5 import darts_match_pb2 a s darts_match_pb2
6 import darts_match_pb2_grpc a s darts_match_pb2_grpc
7 from d a t a type . enums import D a r tM ul ti pli e r
8
9
10 d e f run ( ) :
11 ch annel = g rpc . i n s e c u r e_ c h a n n el ( ' 1 2 7 . 0 . 0 . 1 : 5 0 0 5 5 ' )
12 s tub = darts_match_pb2_grpc . DartsMatchStub ( ch annel )
13
14 # Let ' s c r e a t e 2 501 d a r t s matches
15
16 match1 = s tub . CreateMatch ( darts_match_pb2 . MatchRequest ( userName=' Ali c e '
, matchType='X01 ' ) ) . matchId
17 m1_player1 = 0 # owning pl a y e r always 0
18 m1_player2 = s tub . R e gi s t e rPl a y e r ( darts_match_pb2 . R e gi s t e rR e q u e s t (
matchId=match1 , userName=' Jamal ' ) ) . pl a y e r I n d e x
19 # pl a y e r 3 = s tub . R e gi s t e rPl a y e r ( darts_match_pb2 . R e gi s t e rR e q u e s t ( matchId
=match1 , userName='Eddie ' ) ) . pl a y e r I n d e x
20 s tub . Fin ali zeM a t ch ( darts_match_pb2 . Fi n ali z e R e q u e s t ( matchId=match1 ) )
10
21
22 match2 = s tub . CreateMatch ( darts_match_pb2 . MatchRequest ( userName='Bobby '
, matchType='X01 ' ) ) . matchId
23 m2_player1 = 0 # owning pl a y e r always 0
24 m2_player2 = s tub . R e gi s t e rPl a y e r ( darts_match_pb2 . R e gi s t e rR e q u e s t (
matchId=match2 , userName=' N o r ri s ' ) ) . pl a y e r I n d e x
25 # pl a y e r 3 = s tub . R e gi s t e rPl a y e r ( darts_match_pb2 . R e gi s t e rR e q u e s t ( matchId
=match1 , userName='Eddie ' ) ) . pl a y e r I n d e x
26 s tub . Fin ali zeM a t ch ( darts_match_pb2 . Fi n ali z e R e q u e s t ( matchId=match2 ) )
27
28 # Simul t ane ou s matches − we a r e sim ul a ti n g 4 c l i e n t s ( 2 matches by 2
pl a y e r s )
29
30 my_visit = [ darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=1) ,
31 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=5) ,
32 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=20) ]
33 r e s p o n s e = s tub . P r o c e s s V i s i t ( darts_match_pb2 . Vi si t R e q u e s t ( matchId=
match1 , pl a y e r I n d e x=m1_player1 , v i s i t=my_visit ) )
34 p r i n t ( r e s p o n s e . message )
35
36 my_visit = [ darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=10) ,
37 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r .TREBLE,
segment=15) ,
38 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=20) ]
39 r e s p o n s e = s tub . P r o c e s s V i s i t ( darts_match_pb2 . Vi si t R e q u e s t ( matchId=
match2 , pl a y e r I n d e x=m2_player1 , v i s i t=my_visit ) )
40 p r i n t ( r e s p o n s e . message )
41
42 my_visit = [ darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r .TREBLE,
segment=20) ,
43 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=5) ,
44 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=2) ]
45 r e s p o n s e = s tub . P r o c e s s V i s i t ( darts_match_pb2 . Vi si t R e q u e s t ( matchId=
match1 , pl a y e r I n d e x=m1_player2 , v i s i t=my_visit ) )
46 p r i n t ( r e s p o n s e . message )
47
48 my_visit = [ darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r .TREBLE,
segment=10) ,
49 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=5) ,
50 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=20) ]
51 r e s p o n s e = s tub . P r o c e s s V i s i t ( darts_match_pb2 . Vi si t R e q u e s t ( matchId=
match1 , pl a y e r I n d e x=m1_player1 , v i s i t=my_visit ) )
52 p r i n t ( r e s p o n s e . message )
53
54 my_visit = [ darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
11
segment=1) ,
55 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=20) ,
56 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=20) ]
57 r e s p o n s e = s tub . P r o c e s s V i s i t ( darts_match_pb2 . Vi si t R e q u e s t ( matchId=
match1 , pl a y e r I n d e x=m1_player2 , v i s i t=my_visit ) )
58 p r i n t ( r e s p o n s e . message )
59
60 my_visit = [ darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r . SINGLE,
segment=5) ,
61 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r .TREBLE,
segment=20) ,
62 darts_match_pb2 . Dart ( m u l t i p l i e r=D a r tM ul ti pli e r .TREBLE,
segment=20) ]
63 r e s p o n s e = s tub . P r o c e s s V i s i t ( darts_match_pb2 . Vi si t R e q u e s t ( matchId=
match2 , pl a y e r I n d e x=m2_player2 , v i s i t=my_visit ) )
64 p r i n t ( r e s p o n s e . message )
65
66
67 i f __name__ == '__main__ ' :
68 l o g gi n g . b a si c C o n fi g ( )
69 run ( )
