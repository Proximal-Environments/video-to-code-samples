"""Recreate the reference animation with procedural rendering in MoviePy."""

from __future__ import annotations

import base64
import zlib

import numpy as np
from moviepy import VideoClip
from PIL import Image, ImageDraw


WIDTH = 480
HEIGHT = 360
FPS = 24
DURATION = 15
FRAME_COUNT = FPS * DURATION

BACKGROUND_COLOR = np.array([14, 13, 28], dtype=np.uint8)
DOT_COLOR = np.array([46, 45, 60], dtype=np.uint8)
CENTER = np.array([240.0, 180.0], dtype=np.float32)
RING_RADII = (60, 80, 100, 120)
RING_DOTS = 40

TRACK_NAMES = (
    "small_orange",
    "purple1",
    "green",
    "purple2",
    "magenta",
    "gray",
)

SPRITE_SPECS = {
    "big_orange": {"radius": 25, "color": (255, 127, 0)},
    "small_orange": {"radius": 10, "color": (255, 127, 0)},
    "purple1": {"radius": 10, "color": (128, 0, 255)},
    "green": {"radius": 15, "color": (0, 255, 0)},
    "purple2": {"radius": 10, "color": (128, 0, 255)},
    "magenta": {"radius": 15, "color": (255, 0, 255)},
    "gray": {"radius": 15, "color": (128, 128, 128)},
}

TRACK_COEFFS_B85 = """
c$_4fc{o<z*Txkg^PE{INkS9KboM$Al~j}=iYB6YQjwyNdCEKwAyb)3k?HJxo<~#?N`sV?G%8AI(%bL*o`3HD&b6<7*1gteo$J0`RJfAw-*b$6=07d9_(NxNwRkq8793~0BV2C4OY7RjKdd`8%h;G{74!JL^f@-M<GkiM!fj!HiovKomUH*VL9XFOb8f$(B2Q)_hmE)s%pGuY<iy&~B8OyK>9wzNxUXLlcJJG(obX5$j#h6k+s0|<x~|Hmm)OLy8aRkt5S8XukH>HqyH~S!UIcKb%B?wNvu?44$98k(=_GLNj8bX;r`a5f-Km^el8N-HpJm+mz5blA<PYqIFOi(Y&Kq3Io%^|_GIiW7!?N7%S%jYY)WJRTxfE`GQsN<ncO1Rn+v(<173((bD_ngC;B*zsTC>~qtsNC=Ig1+lxC`QBt<?tRaC#aItgjw4<2`NuO3(Js=L$x=<(#=F!ArQ1!PT3`a<7akawZGTa6>I0a9g9pxz4qkw5w|)YhqN%6{-s1ZnBRer4bTrP(T8AQ&c$D<MtpcdP14*vpdUGf2+#Perw1r;cKEVECg;_fHV85Pk{UEM-h#iM%YogICj2G6}z@=BmL=R1$(xngALbx%pUr_n(k9=WCN;bHusY-SG;{Uy=P@2J5alp(pdMH-BD^!FAud~)oQO1C%15xv+6lK-fzObmtD?Es28)f)1E?m?@soGL;xASbC)e>(WD*TTd;k|7$VkPV1I8>q*upGXI&Sh;A>SoSe3o$5FjhaZhuombne8l$9|=P+7eyX^vh19<yyrK-+Bi@@zU(42PNPo6~rFcGmS29e@{;DmP03;j99*%7vYst8}TmNNk*S+VT+ze!YQqX<kI2{6ygxa2AlW6Sac5whH9wQ+Ri>Ydlw>aWs=!PgyHcAQP#IL4%nk{q%%v52w3W~Z8uXPP$i30&&xrpQg*U0f3<+esVvgFDFpf?E!efw6G83ze6nF=9n#U3WbaPRh1C!Bh?wMQ?AbS;y}ei%R_}@-cIyPdAk>-d-l+l;bIZxYv?Q<;(Pu4Ix&v~wCtI&xLUZ^3B+IcC6en#X%w;8vWE9yI!#7c~(rHr1uLVl;?br(+#bK3JF!2gbg>{L#Y`)ww=v)|0xRMKDMdMpiALtC`7m^77{ub1{PKZ4fxe&@eW|8;=OUMyk$Vxsr3t=bYNvUfj_yvfuS%>36Xw7b-owp5mB6o?z4GstoZ6wBe!XPg<o!zKr2>1Fn6T_27!Pi@bRp~zp**V(?&MSb#<Zkl5A`<fY=a66i2+n^?Aa<s1aD5~h&%K&}oXek)zFH0Vxl({^3)O?)QS$7XGBXG&dXL*tBsi<TA~o}*pviv#KNs<VGxskLq2X>+cXb?>>>oi-b~8kH#%n|pw8(yURj9WbBnbmEpnsP%d0)90hGQO*58Gd&FXtKDSEB?=-CM|O<4|<T>lOAhRf8;#S0uCC38~QQ$$Nnyu&Np*JNIUxKTQY8OXqxGPdAZ!+M+Oj_8iiyu?+64N+6diwIIlF1qr(T5}mT?CF<X$A?=<GnQ?s|xCehCZ_RW;n@@uzWtM_yOg-^dGX<a1dZhODdDuFXL0pc`0;L1GWV@Lej6aGdZ*taxmw*~sSh^TGRBMUT=nfcsB}}f*i3D-EDiY{q2gu6>-z_)|HdQfXWr-mCn12Evp63RVyaIA9z84t?L}4MtGw^k?oP5%p3j$6e<j+|@klnbATz;nw66F{xb2Y)YYc0w6s{#Yvqs$}gK{RqWll(f)qL!FNc$x4TIJ2~dtQ>ugGLNU=;XkP`K9xqChwRavj|{&4Wj7>pBglK5QncotJlUhI0&hB_$v)Xa^lhU)(f_s?{6=!g*>N$Ds``UFL;NARG>MewsRP~i9yhihhMy>zw3N>TrS1u=EVUWNywb?DOLfTIQ<W%+M#B20IC8^Y83I#ei22<MF#Vx5p_A5w-|?qdi`@mkjbw<_o&|7Fx*Uh9nZXW?twdy_JT$Iej#n-|2PYS$lLLvuV7`8sX>d#du@*lP)~p5t!{;z>y+2qSo=#-@rjVvaAf75-0rgtSq{37X;!!>B^w|M+zN<)u*c=FH%wx(c4}irMTXIE72qxbwqlSYvfb}h7;v4k>eX{XpOz*iuwSot6hz~=prBV3dBQMx@GL!_*3`BE8e`25c;c$FxCE2yN8_m)fz~ZMl@co<^sTyF>Gv8WV9V7yKw;UoTf(crAc?>t~I1RsKqe!9&gIaVtu<@TfINj|`LZ*+PZs8~R<h^h>*<(oR1V+)e1<lw`;~1=T_>4c#7XWixE~X-PgQCSea(IJ0{JCk5b(aN!C`W<l80mwTWh?Uq#lb3`Dv6w4hqfG7$CEB+V5y-2sSkLH>J^Q#%d%vMdAyj!-~EPEBf{`bDh^H;3X$Il<LE_7G?p*l3|06l?mR3CdECp)wq6UU-Y-TvO}bI|8QWII#|J*1+eR{Li&5GQIjavd&qJ*xKY3aniLU<9#L3aIP@52p+nadkPk9VB4crKCMr-iG>#xu*y9&&Vu7_SXF*5pG6j~3);_mZ)AU{Wh$nSWAvf?f>?^kVw+2s?s<!mMzoKk80tF;-tBxaM-am6T%+J^hXLm}(BEctempj59ke6T4BVj>!FTc;3A+g^Zq@qTcq^$p%wJPkI79L3ZtV|Xz3ubzrtqot-ZnUiscL2ubo!dMEyCB>Oo;dUX=$?4eS#|I?zu8AS4MUbf<h&vrR(Y6T}Eb-5elZ7!@qv9sYvcJmoGz5aZV-Fss$58f{56p9|bMV^zJ(k<91aXJet+>@8aH#S;b}xR4b_LC*q8Dy}WE~cp=nkUk-U9gam@oYHyoHaRx`^n&2_`T(91h(`!3%ySAR9%ddGSL(SXdOtd>fSpv*dUtxZV&(pEl#d)1@fkxC|~8_ke84@7U5~82vfY%^W=y2K$QQ@#fPN$oute#^G8b%n{JXz2@D>+oF)kUUU%B2X5l><ru~20FLb10WIDYm{%wXlV8qaxzkZl5>SC3eg2J3+)iSyn{S2j{ROzeXbNpUT*s8@pMo~gtN4e^OEjReh-qJR1a$3(@RME<m})zSy&Xg0Q-V7tzlYG4el08CGiTu*FN(QrB@H%9awu^tcZi8Qg}GWEka?&awb|o1+|eJwA@_>WOLKmvODY;-GU{-8%5=Eq9LL-gii0FwV;n2~0;vwaVNNO@fR58QnKH54XbW?V*<u(CR}UEAj;6b4yUQZ1KN1KtS9CM+zaArRo(nUT`S1S36{!X1uAz<HYZ&RK?I2ka%}DMoLq4C1n0L#<;LM>n%!;~h6w_GA{0fhNu4+{rrb*B<^V_Y%oA!bO^O>R)C4q-oMlEI=m~H4|&d{&Xi*<%fIoBPc_lDw^hwD(;YI*#AcQ`=RMrL+YCpwb2g3$@u3_tf}QzUc}?Qkz_)qCRywkt!J-o#P#UEYzg+;kL*zEL>XV>-;W+-+4`lMGWEwDD!%pXfO~jdHMzg3TTmsC>z9==tF&>SEd!C{=sVqVlr?O`8g378@J@(P`t%AI*nIzUdyLx+w+z$Iah^QqcdjqrCJ#j*jDm{->FnFL4S2rQ3#Q$+a2wYg@0|m&09pv&h=}orrar_y+4e?TS3HR1QaVO)fWNAd=IQ;m&Q;+QmJue3@3wR$=ok6FGUe?z01%_Ht%%GC4L;Rh(H=Gw1!E)!f!v5$jt=a@f`vv#n`U9iG$jS)7Wh8N64&dpLOkquddPXWUGCS)PUGTk<+9h<-FK%3IM_$enXMo?Gl(#qssn$*tR2%FeoVhU-)B%PG%YK+_*RiJHF%H)Hlq`qZ^$wC!LQSt8QRTKDzR>go5WXKJy;AcU~zZwPRLk2ul;>o-8alT!9naWw5@(n$}Gmjje7XXT|l!2FaieXQdnHGkkODgQZx);e(mPTstZrLO6*#?A+5xt~__QAagMdAX3aRcM20c5!t2uV8SkuO(Z?lc@vU9J;Y`qt*8?Z_@1R3v)G_;fGrY7R+HtSod3~Hc+KYZPj6C_8{>TUIl(>u5|jIPe{ovl8lV`U>7BIIygC`Rbl0J674mF_TRe&Q?DfuXMYM=GA$Vj9thB4tq+jnWGV?c&qee0FQi5Hyh8mY>xqwl8TPo&M=Ko&MTx31#Oc67WEY+WFTR=}-4pA`eBte&Cj10C-mXR^;htnhVKmAL5T|_#Gf;85GHIWC39G&zf+Z@hsQUazEUg&B$l66iv`Dd4aheiY@@oJ|x3|NeGL|}V!iCtY-D$Op`UP8$7osNBnMCX?4=V~bKvw2zlomUVZ{0l5di_}#9LN<%Uhb-ddUXID-B<}NlO<@ep%4)m<TA>4`oS*s%D=fbfyG@ra8|@+aCs_>Vs-nm<Z=Prx55u1woj*og9ov8ffUL$%L5&*9U`gx<jQ>+e4f_?OK}ydUEYLUB?j>F_4(lZI1*(@KgByM{qWd=t?(#jH;P>U5a)b%usWQd4xfBH(1PC&u~SPN-r#r@p1LR??uG{ZaOxI*6dM5xY$>E{P>SOXt+5-u4TjSPsCls?xWEFpo<0x^PS%su;?7chts)C=yL%3dRRWQjTs3~|EJ+qhdcrHAn^dbz33l;z!oJR%!8rX4QsG?1svATYSH>Am8=E8bmm@eZN)Sg|M?g*LHl!TQM_h6r;;E<GVCGT{<gIxLUl7R0$ZsVi)rO+WyjJY?XbHY`elL^`tDvkP8Qi-s9cT6gLz!+lb!@R2PS%@AjLtbi{XIT3ZI(DL5n73*H<*E-MJm-gT#W-W7h{(VF0k{2H!8BZfwhhHWA?Bc+*c1lCFK>^Lb@AYR9FYwhs@ERM}hd@<~n?|bOFdm-KK6R#^OgIe0a2SElBk^BR#$iICrNruG`@VBA?1p9~H{X>Kn&zHtT}^+4PozRfP=y`pdX3Vg+0aJ#Y1H)@Md>UJ$0M7eInnI11gUh;I)jVRqhj7!O~9_Righ4+r<--Ga&>v-1Zfc}EtDviI@uqF*R=Obvw}*^9Y#x|rL+4|c!TAm()@K24Y7Js+3BcA01-y#G7%Hs~W>D5(i9LJaj@Wg2BEG=dH4zajT`htar7BU7PUgpU}^0^x;cQA3h7K6@?#uQXl=pA)nw0k^@{Qf(Qs<G3VrsRdBh%daq3kH5s7V-x7ypB8GRd?GgYE5i1BXTk81Y^0WS0goIn!}V$EVDeoOT}$17d-hG>sn4<?vcHC!RTY72&NBFQ<Qw$<s3X;La3$v7nT*XIOb6E$jwo>JR{YJe1#8#|g8kGq6s0;1i|8nm=#v9zMX59uP{)tEJzwLX_!mf$h*M)TUonob6GuO|jSSu-P`M6{Sm#m+j(w;FE;s{egq~qOe(J&(>&DRW$o;5QOp4M{&clO^rAXm#A9eKje2f#qvA3!a++1#eYI64A_@iamFz*kt639YP-|Cr7_a#ZIb{iTsGDbu=lgW%4#(~KlXiiN5rM#KOYa*g?dsHH751^?7o9{9^mJpmc{|d_ga}LeFn25joDUgboX7n^vo^nfWZ27DA6!Xu{M4ew#s0n#JoPDthmp-dOM|bs8Z=bnf#ffC>m(qm>0~C-><qSOINGm>0Jw!=n7O0jhi^q??!6(bpkm#y#EC2V?aKw^Uyv~(}a@74O-jYX5%`Oo#b-o?-mOi9>{Op;*xA$;$e+L@q6{RkjiQ>~G@3C$2T~ube#Y*&(JzgL^fyXb`qSW)<R7O_;cANTukMuI=jFv6>gJp1GN)z6&x)R|fGRWuBKx^L2?-*MvBEPrd$ff)TQ>8$#V?iq#2wF}h6d$7Qp03C93qw%klr;Jzv<{!!Ig{KwQGuREsiC&6LrjR}5dQLgIyxF)fes1@QX3P3uvn}Qx~w6Hik{>#)t5W)adZJ?t>1>^{41EzOCRyg(lo>zh^O3)ikLN?^*DZQDHSQxPR*V1x0TxwkI#R*hHPKQP!~?zu~IU4htGTYAh$|&WVh6nF+ARdU(0SqJBr7tkF(ddz7lH3InLFH-Vlz2RTP=+!#ViOTsaiERtNohx0T7<$VakXh*Iy;pHqTw1{qFSC!UbaN8Q!;Dc;9(REtm-PWx7j=#YiTYehKjyfBDc?Oo7yYRK~Lb1S^)`h9F55Qj3RjF3l(7*14a!X8&LP;8Jm`pSG{B#-{ZQt5k9so^=4GkM%xb^AB`?x{KoT=SJmN-bb|T?X-j%e&C@x%?<#T)|3ZktCU;cafsc@wXmr7NeGnJj3?Fd(jDZ1GGN#g++W<Ek6ACD7xHsifV8b!t|zE+<ij|<qHc?7nRbOkc>&}`AY+p<{P08b$ZmwD=)Bcbt=01%p9G(y$)}6dyd8ZYN(};`>Ei$4a|_=H$11R80~)|kDlHU#BbNAkxk?BNO$-*CD<rr^-16!j=Qpz`fM+RIJT2kgMT{ktBIM&Q)DqRF<pi&Up&Clf94|Y(s8Q=4)x5SrVL5d)I>{k9#Q#KwTzzp6Re&y<Db_x(P71=mhcNKj(Af?Me1dtwFQJ(Cq05kJeQz0#R@9^`%LCl&j%d2aUYd)b~^H3t;sx+dxE>S@3Z>LoryFb&Ze&HsKxe%&#ZRe5kmFS6yx@J3?H02NL>?PsM^fw%o^9%c;drn>b?0a#Jz)BDXSqo8D86Z;$RQO%?)S7CnE6GM~l!(i+}e)Nn(B81b+474%HR$hYA%@W=2lk$Cf%3t(GA>(Gi0fX7pt`j;KAv=p0c-ITzJ2+tiJNzQ(s)e6bigH>6Ya%*Xh*%NwercYyl7@C0RkNsc@;w`Pt`il9h7AFI5R{W$#77UukR2XwCCY-@&34VK>1Vl}AdZ*}PKi<WC)jd;HDel)J;idubJTaEwuhi}8SmhA_-tay(_m^}~P;4<5^Rs$^>8Kqugyu`=xkJg=5*OS#z&-}Se!0j>Yp`6#sttg@5`RAb9uJ3Vg<XuLxaDVf=4~Hnjl4(T6Uf(KSb_>e1Id3)VOe=O0JVnhgdP8mgT|h1L9l_7^v#AIlDRkTpS(Ph`k$v6*lxQwPc^9vx2E^`SL81E$s<=xvu4k#m;SA3G&1dEM`XuUzWvQO7zu0DlwWWS$vDN>$IfA~6|EHb5FaO8UC+d&>r@QViZu7_%wYh%$ymhmIkd0RTYU|)8b<Xw#JGz(qlP4t-POB#9aeUl2TPGEEb8mTX<b3mcOADz0ho1`MEIyh<>#KHi-d4Qj{#{wiUO{iT<}WUD9ylG~-WXfOd)Bsq=cc}oTkgSceY41xw_wv^ZfTu0ue9FBx+cJ!TOs#|v&=?`H$zL!dR-Kk6MRO)`lfz1EBnWgBi!?qlkInbv!}_N)3Nd}n;aa*vA2=rDCKK$RMvA?uYp;dCodH_d)iIujiaB4>e+7EH$#R~At%idD^6oK{^HS$b0Z!7Ta(kX!;#hBE=MZ_YLTaU4YZ7kE$eOj4EZhFM>l*vLvu>Zh^F!=EIbuNI~qjN4+`Yi);HHsct8_~NAq#+Z5|`Z#wS70O&Wr;57PWMUgHHm5=3HK4cet+PLFNRBu)!WAtu$C_E!$3)68|rz^@(@_f85moJpiNC6yETO?<>WVjGqsakTQWbgZZ`hL$>CL2H8hK;YsG@_BI?cH%jLg!)lBe^nwWJ3N83zp8>!&UX6A`DrAv_79#yv4sDWDV?dUO~Pcj_>R2+9Fvr$O;vwb-E=fZLAn#DW8n-s{fjNJOumIf?p(C0ulA;`)8-MEyg!z9CXaAf*L~>qsj;jXbR`czjxY^#r_=KfF2UNb_TU3qd2o?dq#MKQsJqUe7{?(&vS!MJRv;`k^RK}XYJ(VF8PWH<elZ-4My4?+5K9PWfV98^rs-=nzB#cE<+Z8No^owiKiHefOId<^UdhmbU$;_j|Ck2MN=Rp*I32K)!P^3EGoQRe@QL7F*qL9#Sk@kFX}itEqtcflLiHgo;0)n*UOrY05TNU4c;RJA=~$Bd#I1pGAaG6rMR@a**z}Ls<Z&y!<ZZ$;zY8->uHoq1of^nL9?e|apM-_<<`KE^$1tuGi;oun#9^aqI49*AbZ5*##|u*Mij7iu@3phQx~)Pyi444WmlK-M6sI4*Swktc=Th30$=GMv3vf@~LV2hGGj145)}{4>!?HDaHG6{T{uGR5U#CD~Wueuqo<EF}RReb0Sp;V;+hQ+$QQUSU3-_3PgEOygFxB19tqOZj68pOa@Y-Y%)|2aI-V6nig(C^@V|ywNJouWqHqMU?YxN-fKFc^*cVqhWZ)~_L2&yU_nPT+`>@OONoiegPbEzUyR(8Tm74GB7I|pEnuQ`*l)(!g>T*b6e85CWLw`zT0fh{Xp?054Rl&(vm1j>W)M2R{XI}!#d3olVZJJPWA>fzR<vGEX`z(w0+G?|q9^;lD`0XlMDSRLrHqKc=@B?e9pVQsDyZk6D+aQse^m!lh@T}=>|_%CNZSD6v#2nW!$y2j|-JAkdboN(uW7sQ>SvG>n3{8oD-S+OP#%qESQQ_DXwL2JFqRjIS^)Jh#6U{Bzx`De)L{(H#%vnexDo`v6pe8Gpkzae?gD$0f)!!lyRcxt~OOx2qrL$NIEy!{u}N!kY`-x##^(F2C!3&kUA0mjDOS&gh&!1#s!#%SF>xXXD($=~3^FcOCOlLFw*{z|GXT>#53>BmNnF3>D#g2LPFs2K|@aFlE`s6O&UF5R+LCy(-zHTTa$Q+p)SBN$7CXrCg1)rqk0({yb2Rgh9uJVTOd&B6BXCFWV%YRoM&A)5{EqHNbR>Qtf#{&Vp@HaegJ4ZPjd-j#>&202CY;=occTNT1s?HXbpnC>O}d*{G!mAV%0s34Yot3t$VqmWoZKlQaS7BkQLu*9u$R6U@Lq8*Oln2wjsLi0Ib+qDrrJm1CKI~0Or7p{X%s~b?G^EpPg?miB`vKv~TNujM*hg+8W-@=^fM)2p86eZAJ!Te2lf$v2wg7@`B)Y=tqnC6-pWdDiP@YT+g>Kv58x0Cwu@lEb9@Ti$O^h^mk1+66ft!qK^vN)ckspgV9VZ?U-TA(T~VABuJ{^4IBxgZ&WJ~YHIaNil<`MaE4QWHn#E%YgdU5z8Sg2c2W3+2WKQ5*l>XYRk}BYc_i@cx|=^)_7}f9q5xRkH`s=7D}{hNmX(`8Ja@XXqd<)<kDz6Y)*c%lP-Lt0-Gt6Nx=Jh?`Et;vzDNTGzLu`&*v1TAqK7ch7KwO)bgjXUZV;-fbEYIJpE=wr!#GL|l={cO7zenJN?&-le>^=Tai0dZZy^Ap~8()Xj;l)Odm(nJ4rb#ZDZgR+!gW8Jn#qD|%!g;CL;Q>TJvWN?uEp%0*$#C<kZkc4ktdB1uyoL3c_$m>v56xUSuiRM+XCy{@RGKeh;e6)+`}O$vBjOeZx^?uEM(80_asP<&(=74kg_Pyh7`8$^YnMFIb6ZTfax?IuGyb#9|+*Md;O4<55Sr44s96rr)XPLxrlB(_#A#5Pl@NY2>~O}DMK+9q0o4I<=0-aZmNovuJ}>gSP<tST&14n-?d?oq_um>jS*1CiKaD*BEP6?spF(9cFt>Y<+26}vB3&A8%Ag6jD|=s*oK`v#B6ZLlTY^ca%b&RWhAIl~x?xDmEA8P#)4TF%(0piX&nLUeDV>~K9s;CFAUn5F~Sw`$Pp>y#R`&HFGuRcBA;-JHt^_0Y)7lg4(d8T`HL8T0U%9Wwm17q=JP#(7dZkk0$X=*k&ehUH^%!M^86FX|_y(J9Id_T9&3TIW!Y{Y-Sf-M?kuaRHL(lZd{4c0`ePw_A;tru>@+!KiKZMaucX2(_t2lEfbp2l^hDdi97<dotuno2woe@+VTq+UhCYnKoq8qk1H$mdDI}v=9w^av=Q!S;$Cfq($fOW@b;dJ88an5S@M#ZE3+V#+TAIk%f9;NV_hOT3~XG8M`%~R1P$^?p29r{v1@o))sR~jbNBrOh*WlD=mk=ifNIK<a#P)&;r>FY2gOhKltirE39s~5_!Csk8?kC;=zkelt<1MR7XVdhR!_v#cPz3%@jszeoq+F^?f)jvlmUb0`zVAB?dW-;`E#Ds9ED8lBv7ZlCe&i2qyTWgAX(*Gv_wyROA<Y^<QtRdSqxNa5;~1X_h6M#0$|nNnOk2<d00m{xxI;#h@}PDJtWy0h+mH1Hn)KP#+#_rW`CInE+`gk{RDX6+5V5pYoNAb-)htZm%q3_VqI*x!_YvW!+A)A%!seqC2TO-@Y;u71G3b>oew4s4+TdqRA}CmL!%n|Ip`71~q%pS=?SZhR0tgx4hrH7M0b`W&#!n5Z?V!tHE#4=s^4}=IHzeoF5g!3?(?D?E#*Q4Sy%Ln~*>O593kJvkb~X;|AvYd=w2f-lTrG6}C>#(jp#zxX6BWl9j&tVl=Zxmejp?P3>*;LA|dfkXNZbSyQ_JZ4tlIdULK6dVJBI4EYozzgs!fx`pqk#hotX{B=>JBILw;Q+vjA@U0@dp0`oAa}}*D&ZkjE%hr)Q!U~K~ur`|ZLmn?lSVX=mnBx_@hO8?4g_s2oRLRlqc&yMDgqp6<nD{D^{mUY8=z(#{cX=?Tp$?A^8(`|oFm-E96f^qk1(q~>YMHL8j-E!$YMngw=|7HsyGj1P|I;lor~l*VpH*4^Y4hShn{UUD^5$N0whob4)Ak0oSbt^3tyjYU*Rkm{XKnRHVx#A1Jrvo+Th4TFlU}dpc|7{fG5Q$GQ?_m4&A#l*^T{>k{*cMQhC*DPS(g&eRZo*=*!r8ZL&J^t(@>F{EvmvhHm!gYN4Ic)zMjJT+0ER+FFmw-eK9w3)R$d!>Ks?#K0ik$s*dYCzkuB=l*CQEv6SOA5zHM^-GbX*#B)CvKcUesJ?_%DhhTPLBiFq~hh}|Na3^ysanTk%u3v{gZHzW>ul3ZCC`S`+`I-hge(yZ4c(4>itup6Ip4>rizWsykesB-s;%9M(eh$E{c|zO+yC0$R1Ao{peGBLbt~|FbSs3r{5#qkgIZl7RHOanT?FAx1BHZ){BbxvHZMJX4O(?nWjvcG7hC1G3wkp*c8js#)8;57oBClSvn){5A?V~4be%*3<e_A{1@gW4N-Jh^U27+|>jbc{j$~BljLfG6@*WvB7T9zcA0Zr`+R&DDjtg>xpl|&RkOs|Tq&Q+(E-!EeY&V_+Q={44~?H4@NNML8>)Pj%p1-6%S8D{-VW{deFLBBqcbqab4AI{{nc4Gz*)tSN`UMf!8?TBORe@DUY-P!EU#SdWQtv~DFUIf{Nv8>g?A}Ie5!XDie47~S2tmm=&VEZAO^?l?Dm!r?I9zO(V(<T0_QBWLw+7-ci$#%iAVn=rQl?vz;KgQ16Py`e2_ONQJ5`oP1WM_YCf;XR!vO^|ruwHBzTUPlTqVm1jpSdw`rS=H>I)(*CbRGM0S_4ShZeb6&<-xQpdp3VTD&#AyWe-j^Kz`*WHpn0dYPZ<3?*e+kjt8t#Rw5{{n^-BAYv2`c%x2!MfRGiotm{AuJd_94R4oO(rH$BB`|IFSWX+~_h5+9abM^;w4?=4fvsoXb!1$9nJLuE`_MbIazJgL{S-FJmKb-{6LiE_mB^TiAGi_GTz7Dp^FJ<euM8IUVE?dfF!Ju7})#;6eTg+nCa8C`a@s?z-{kZ}i9dp?l!#pS!QDjd)NCa^mWwt@59Q@lgSlfm1;D1(~b=`dn;txr%p6m0#`GO`Z7m*A8PXyQ&lVq^lqQ>?z$&g(m#a8GSfr^hX+n19IvsS6HGMl2{qP+_H_uDn7R-eg!otF<K3bR<=-Ws^s@|PSlDuy2)gxUA@@i61rG<L8l2?`EPXG^bVLE%*iHs^Q}Sl$q2{rMZ=#Ck!tIW8HZ5(U}(gj%SVcuUfIG6CE2vA@OB;jq$AGXHQg#9MqNt<$ambKon9xElk{$37CPA6Mb<nn~id=OUb_`b9pAUVsXfVN$R#6|~AflF`u;h@SU?4E;`mzUarq^>Q)1=pG^~CgMRlw3AFczXk?`Arj{=LUGFr@=GWa{t7mer7H2TT5^=wtEa>G&%5N>oOIaSaEBD`zX)ovy=0qZ9;{HmOAMA2f%m!_L`AC<g#W$wtz`~alw!i4SPIHN2S~Yi1{ChABkL3rp+UNp2+L<d-I{x(V^0!99O@*pLD`@@9h1D7$q?txBeO>@z?>7c<bi7zuormb77l}XcJ-t<FB2Xdzd`my=7U)GMG_`k0I7rZWWmB3SSC|Leh8(*>`T|l*09TP^3g@2Vp<7HtkTK6${4sHo=29i$cES}h2&y#A*7zGB6r&gVI;Ph^p#daxqdNGrgDJq?G2)nQ3Q9*qY3Y4K4iIFAu9s%VgFDb5jdI*Dg_saA14i#|EVR8Yh$44axQ7QUJ4HfB1!!FY`7qhN<v2SVWZ(;Qr~_NrkfU#XV#f;NIRNDoh*fh$n!+-!3F625KqQTE`g+DK2ZuU0$<lt<i}tXTvE#<gUtz`{3w8|x={o*4>E{_PAaq-g^~lk1(5LQ45>R%1nc(1kmqUTAgO$w1ncC(>+wKR<ev?nmj{tMdr~1y>@?ByzW^UZ!^lY0c}S5xOuhxCL)ODEa=bkOwqH3#UMl9m`Cn&=ct#3bOFls+^YS1!IGoHrR|rO1&yp|aFM&wZNur~f1mEoT65o{>5G>+Egin{i)7ag_QY;IC?2eGOH<h57W=*<c)8NeqU-G%E2!a>ckdR+R(C@H=*cQfu_H;L5S(*mhVm6WXsS;@3zlGE`rh(bvjpR&QIYeG^Ao&XU;B|f%Y5(^f=Xot9@~U|-<_^R#A{B;f-AJ!j4mer4k{fcFAT?(_NvX|(4Gk12^GOEd?dwR*w`_P<zL5+mC4h~ADe)*Ng8M~ogglG^5L!o;J}!fjv<2k;muOJ;(IEXlqQTWuhs@uZ1%}yM$iCG@ka5hEM0aJtShyZ3)USZQ-<FUKuJNGNGnaI7vcOG1g?Mkf2nmxKBymmw>{LZ$t!gRIuZ_r)oyD+isV=!}oDO{770GZ#E~JR-6XpF$pn*(C*I*jBKGP=Eo)^JiRF#bQ=fb&nmgM5Ed^o9TLN*8#gVzl;^5jJ({NAZVrm-1NesVssyOIawivY=pNr9S=N~Ekl78Wz(xKlPAu9(V`rTl3yks(Wbf22U8zX+k6Qej)QDEVYv483Y5#C7aESoA%|<xDO}y?BW&PM?QM+x}w7AF1&5mJIo$SPrjje_}n0eDG0{Au5-m;l}>2cy3re+zR}GCoW~d{fN(a*gpj>nfBwBf9L!@^c)LCr+|2(0P)O72jLJd-V%2aR;{^<6Stj*<_|eoF{BncX7=NN%Xx5H{w2=vE`(h9k9hUpRJdWIK%URdgX9O(NwG>13`Vu%#L0A6zTq=oG(Q1K#B(sa@e-&A#NtzBi4eT^IWB7~1LgW}SngpSz$zBE{x6Tg{>El2GT`fx1f2FQ9~|C4z^O-~V0>jNuK1k?I=gdl%I!4Z$sWRfN&o6!xCPH{kAwYJN^q@UENo2h!=@i|z*_kne%zD`9)fwesVx$wSy|#N$pYwi8pLdS5+vkYz+`p-#FR&2^-HC&tmPtRPu7CH<~|(dk_ywzlCYLR5m?&pz&jqrfW;RBymjscXuju*a|H5XmCzwPyFVWa*Ja_Qt@*HR!8x3okO!Zynd1#v<uJHD9E*t-K%-6wHWA5z^tgKFf>8y8ZJ3V_B^7{Q&?%h$I2+zv^~6$vX>e@4H`61T4HJ*e@Z!W0xHT1rUv(6NVa;Of(Nh8eD=hKJt~|IWy9jUZ4ug$v6Yz$$|N6yt1+3ar3@Z#Ju^_$(<sQ44q?B}MQV+m~7v+FP<2L-RIR_f(E%+ytgMuvJ^7-*_mhNY=epP^BcRmvvk_9tgQ&{y@7IZqiWUO8kg69t{JXBr+k*5~nJkMzO%_obU*)-Vqdyt9H%YhRPUQGL^JaFawWZu?gfx+-EM#ZoIl*=+0z2P$0J^qLZ?zsqVOJu0yLD3+&H-{PjT?j#@-&&7^CBV`$H|Ey!0x-O4!HoKrK&OHn_WGU$R(qP6c$-Xk;giOczAOT{8>{ioD;MGBX4%#?xmo|^J&IfYKlkxLq540LCawRUpXN2MXuJD)J1=IPRNLBP-ZuVitsKW95gUhcPixUjfxNvhTzQ5)Qr2Nbvev^9DXb}-$R2D0?(c(DoIKBP4nL32+Rpa|hqZU*t`2PEtl?O(K}?ACBK_GsuiSTR``i<}oqUU|<)(PtYBk_J6prE*mc($s-K^x4p4`tHeA3Camt4)8I^bcguK9@jIMIxg_*tCCv$C?jXl=tWHwfd{AEUToZB?8rNeqYogapSaBZ_tO{7!F9ImY=_!OwY!YgqNQ;+(sIQk+b^#hiH`_YpxsagIawYEER-2wfWDPhZbgrF)X?IQz0qX}^Q|w9>+>Smo&yt@naMUv`)Q8|<Dz*xpoH-=Kh=oIeB{`7QLw(<ije{f+eWaX(s0n-8AhZ}jEjQ{Xl^mrmn1CO1aX=(ygS5VyY)IH8KLQgaLK=e>l^Fyf=l#-4ziRuX-0-DjA;dOe-rnu3BqSJKB{cA|MgTJ)1JOQM^9fW8pn0_E{Vps*<mErUh$4AFbwqBxVjD7zIr4|&lkX5Nrepi75)TQiNJ=jgqji;-%H7`=9$520qRq}ObCfi4(chJeB;X39^Fe&ZJb-_0I?tLX!D;N>z}^OYFL=S$Ly`O<I&cA&p3lWVQJ{vPUUT*>wrbvpfZ9dee=g)!eBmZR+>5T`{$?51|O_n{Q!8fw#d{Y@yB`U^RUPw`H1V|s72JASp|HZ&ewPF$>nXouhLTW&u~g)N6TIQZmi5Z?9>Z63hjzAT-xS|CRUZc(I+<=?=jWjC?;Q!QF$Fa@9VzXG%T&XR}8eDpcB>3D{JC`c@vz==aw;a+VV%0EyEEr(^OSw}`8?dC9bX3k@1gvWTQK#VrJJ%kPFV<39KjBo-T1Ei?nuRG7eTEs_ieJ<?w;-HhW(_n1CsCA})2fRFLMxDrLfHhb1afI+kh`!N@KRhl0p<y+$i@gnHKaOHSl}(UB@sZ1}Wl$k6-|89@16kqg@Ov!=^gESsZc;v|pAjcF?Vm&JH3{NTpA7HXOv&Vl8?eau7S=2afJasH{xLuybk5*o?7h}PU*>J>rBn;jN6+FbeF5-uvjkCHcpbK;yJ6qCd!UzAChv}9gKcI2K6%vvJ{2_K@0S01ZpBcmG4TPz#~HYzvl4z-m*T$l@t`321z(aVfy>wW@N3o`CXfNSQ=9_FTdw1FepgW0EkvGp1Viw>`S^9b7Yxj4!y*UrA={)Hm-0@*9j(Qr!mbFuf3L-dRvSaHh7I|vei+t2D#OCMOW~XfKiT}t1U4T$jPL5MgXiuAxV<A3p06**i9e1(`fp+4+)xBJr`j>cMjt+WUPm&I1i_bWckr45EinA~0c%=rf>ZmCFw*aIV3Pj?6IpczDi-!(JJ0nX{6&$Z|J!}yw%*2z!pvcgqyfn;je(9s0wisX6u4}fO>T)>!y7wuJWWy?$fM`@+i730Gh^}GudBh-LX%XiI0tj5_{ia)C7>(8A-?n>sNMDmXI@c*moc*mQ?Cu?bt%}xM;>6oAl`4U2W55Hc($Dpe7in@7aw(pBaUM@o2vqOP4mc&R%;kHFT+3DwZKGLg52$13=V~9_`SnyC{Y$7^A)xL=Up7`O45e(QYm7pvk%sUU~E=l2vsfG#Np?9XrA^NYa9~<r3oogv<pCXq!VXskOvKC1rj&v0{7;;#B84eoQ$4J#%8UA>u-jz_p_hK7pw>`ToM|n3H$_RfG7V<qU1A%qW4td{<QBXUAF~G)|o)zfya1BnIP=`sZ10)b>Pz0X+$_m1WGbY$Q$+ffE8jeUqT%+G87>X0t6tvt`vVP;e+kpWr)->Gg$wv0Xr<#1$|p7vcGyI+?_2!u5A$jr;{p#8#D`o90zg7l}dEs%~E1@e+WhQUco~&A8fN%AY%I!z%;N6Z<~CKWHm&H^$k-n>UoTxWjsIzKMcvXt8%c(y${b@*^h|EEaLfL0<9=0#y>(Q(ewN7uuk_B>PA_(UT+8;iMfDBAALkO3*X@~!52t<x;9xZCJ9w%KI5joCWKgdGLHzr?pIFOzvdQ_sg)+P?+QafbuV7GM-&bes*pkTIS{l?j9iK6LN*UgNSTo^bdJ2k{0nnYgvA{4vVJ=Bu6l!QIu9YYR7GMR@CIE?<|k&71X0e4<Y19B)QIqtu-p`Mb>&jB$My;GoBjm9{&*g3XqZ6^50;=};Rkry*%EYgfiO8SqZi#;eIG0NW3+zyJTlh74-+jP@y5d$XoOutj1})8yK@8B_J=z{Lh3}ughfZJ#_?5)IMi-7jkpR{qN{)3;kl`isLfu7<o}!pI$f${mSH^VV|9r|5JoQyALI9ZMM!SXT+)=?h2~M+xMue?BsC;XOkNbB#=OT^?Dris=BQ3m#vY^PGsQ^n#Bvn#)q#B7)rlqyFJZnxgu0gN{$pt))Es*iORcj(x9w&Sce^+w>d}as2fEQrR)}!<uc49e1dDxAMuypjBq*>J4fg!O2ZobSWAqZDdms=U`FRazC>}&wpJtIid6!YLRzGeCwn0DN8xk$;OK8{EnWVWf5cO}6ChLc)(7Yp$u$qhz`aY>kx;LyvPQPyBkkACQ;G;O{$2EuqzQsocGmy?KY2uUUgjN?1;JvyvsAWW#v`4t2%SWE!qmScI_f`So+r9(wMDF1|P>V8u%aDQAV@P-TbTaqcY}EO2Ch<-2Kn~fWMAgOxO?@;bvv*EI3Fk*JPv9UDoYEq@`?Ar-6F>0oC}lKHSB-o*X@W$ieZ;26;?N&Q0aBEE13g~x2bU)sqHCS%Bx{Z}Ix5nI_bzuqznnCP&qp6bo<GG_hfX2=aVcVN8in{XuHzmnbL4n-CUFu>M-R<E;NvHjA>lbn#A&V>imxriA5IIRS%<aB5n~%_b9WE^vX4f^Pe0;4-J!@1%^)WGtkFiP1w@r~Mf)cBiEC66b)4Nm<o?*9My>nU*hmS<+M19%vGvpd{|{V!zMrbOI+M(Z5kZ}21c_azFB-ZzgA85wMDDH+aPzM=s^)_pnfYOyvaA;%>vOCqUbP%4yCXzBRP4hSv%XMyep+O4sTTU$#KZkz7pY-~Ib=qQ1v)OHLDtSZOI0r8BQ8znsIY;5yVB4->J~O7Wfq~-+IesBYMU|YY8XGcs4j=%7U_^&gIX%YRECsA?njfhGNik}p7OY_Kx|9HsBr7w_-D5Y)y*eEzWb@84$lev;;#YKrZbJy&R0Q==k8(WYEkOQ&N;-xe~?-fE=e-?4N~3V24rXZ4J*DI{dgUl&%A0}PTZn-)Q+Vc_-@$%6)vYw8lws*vx9Qvdbv4r<^1!Hx){<@eT1WD3Q{7~ro`B~kvaydWKWq6+E`^wYV1?2q780gUeH>r&fSW{<Do6H`QO|G+4HRqdu54_h7vQWGm1AVbWxi{bV$>y{?;{34{#Sd#AM$PCYv?183mUI_+;B=tLtwhh^v(xis=v`U#{6vM$3%J-%EVdIahJ=KW^5ZJ@-E?RQvz@v|VJ#e>%L(gX4T;2Jd@(Fj=oM$XPvVVzZ@0fh(DMll$bQTwC+~7d$urL%jR)nY=XtJ=RO(ACrzZvw6#sE4gpA@34cNvpC;9M7Z-$%;WeP`*5C4mt{A)$Z!mDp0nkzUU8C+L~w(5Er&a|O1Tn=L-a|k&W$he=V~2(MauSlVKcvpay&epxy?SN9LZu6j?7szPD{xrI=E7fyYx&ur{|Ca*H<E#!>j4%4j3(@4Wb*lE>sZPzp0B2Ia9%{%x77~zn8oIT`TADL2owtOc!Uk`3x7h?i{}iA?sh=pE+8dWgIEaYwnZp^41&Oxn!58fwiml8s5XDORU0MBzRxYYfi2CPwsRXVP4VXT%NhsOJXzQFYX_f<her+cThi(%Piq=JW@)zz3gUgi+loi`DcoA1rWFF;vDYIiL>0tcU(EjyT!RlIh|}Ye=K+4*HKPuxg1-~aiDY+gSnsIn{W=BoTQm<1A6VGK3873nT|uJ=sCeNf$;xg|5BB-^NnYaoRP{*<x6mdKlIWC`aq|+2+?gLB3$FNI67%-0c~MpMlYXiV1;a6gKI)CeeGm2R4FB}y;jrc>iC(o(5k1XEU=1Q{$?XRvCoWtwP^?@#2eYq8shX-kto_rUxiM~Kg+IoS%sEubfmpd4D3>*S)-Fa@N&<05D6_s+d|K<4JW=rVVefM?0h?{JeA0v_z(^vn|9DcO@HBP{(AP%`wC{)k_B|DO$2Oe(q?Vc#?gKLUYK|<1WMr>*)Zi&XdRnIr`VLiaLIA@$znnHE4qT#IWY-+qDJh`f866zAVXWbodz#Wakk4#4XrZog$Hvc(VKZjtX}v$=-Bids!kNZ9ZQ-Ob}vR##+vkE<u34=l3*Xc=*Qs;X3*)ar$JHd6Jd6(rQFpj;Y^M=SR^a4A6|>XWXUl6nwA1;g$r2!8<CXeaasEHrwed!rT}Z$FGZA>zl76+$KZ!wKS>-ogmp)A;MZm~Sh`$<b(>v|)-<tT))fMqYsFcUecu>Yb0PXnawRNI8zXvU(u7&t1WUi}fJpNea@k%7n~5jFbHO>F^lFlP`mh2Ophn<Y2Z6?ynXLECb=abG0Boons8tyzYwM(mX;B%3uG<gWrfP|f><PSFB^vf1JrHc_BnRtz7~v<E;pso-eW>+`oKDfjmUFscgMBJQYhq&SqeANP%D|xD5NN1Wl4V}qczJd>d^)!X%+d*w`TLgHR}cqV#)815pqGSfs=_TR2n;O9geMzrkTZ@P;wYF5YdPEDxNQbWuD_2*>`wr*b0M5Iy+QWRmBh3B62R~IcGzEkhq%LCymU(~+(=7=Or3nf*(OZvXC=U*c^)wLKsLEU-NmVDK42zh2*M9jNoG_mzN8ojO9BEQP`ia}?`y?xBT9jrln6&&WD&k*UD9zU6hx++;ibh<5;1=Uad?ejxsWsrROFL^gB5sv#lPCDae-;$B_u-a2VP&B2DvHmuwW{K>|0_*u0-yJ(3b~b+m0RN`F9aATCNRhM|GfXeiCtBa2<c|-vw(^jzN)P776a>BSM#>z&S7gJ{uh)j){82pV<K^?)!mHZ5Q!g{TVNPI~%U0TER;aMpC|Z;HtqLu>0CBc;|VJL|fM2Ak|>#%?*dn_rb(t8zN$cUU1EJ58NHLCwpE0;G+*`fp?k}tVwVsm)UV_d&doqffKCE4I@JWFR|x*SJ>DP0-{|Gq)t<fMDMVN&=6OUV3v@+P;o-`YJ=uY1X<;q$oyRluGF@G&E4DKVu&wUu|$eEFLZ>-$y2cJn<q&WHzP{%iclTu2yWAs5hL5_#7FNJ;>%tSze8Mz4V#5UVvS&s?*Pnb*h`H0r;!W#X3)Ga0uF7rC2P*FAnZ~}c&p$ANy5ft=~X`R@Q^sLPG+#@#aa^a@g=rXTMYM-o#2t97ioPdNPhiT2jk~L;F9|~@_E#PY!FxmL3KV*-uD%2C&&`i@C7|Pu?{X>F(%h*M(~Z*>Y#RL5A+w?lH4R^QhMDIV%Za5LuL~VU0ss)^xr<A>jtl4MTpi0MIs?81n=Ijg%3Y<N#NG^m~f?`-E%k8J~SXdmq?Sjk0qc#{wzGaqd~Yk)rfK?KWu;I3Ol@I$c0`lQrldP9>p$)fZfx{rz0P*srNS|^u`txS6Y(UJ%VKEZAG}ue;QIgiIcVx5AtgA7n)h+1Hn<l_@;^`Ii*^Mp1ya3AGfv1$<@#B;kqB_{$)1^E-)nBTn&<+Ar6<E{NUE*>BJyLfjsn;0N-V+pvsWNS2Z-qjQcl`v8*#dr3jH;H;BvdXSBv;6}&8!Ada>wB+fw)@=c=PM3*?Rrxy?vgHg0wYZKhO$Y9NdDkOaC1vJ`e0^i4{@Q|e3KM%E`!4e11rN(jQ7Y$POtOqrhpM#w>;$*YKLNeCSiSDOtfwOBOaAKV%dBi)59!oEUsI7PL<->3AoWdq_8XpJw&~fasSdP5CHjcFR?t=ddOart0>F>3{x*Sr%;gX#}iQ;cUZ?o3HJ}M=`>VcX;`dVK?L;|eATfZ5?+q~yNrFm*X?duT2PihpxHc!1lprl<w0Tk-N7x^&4_^84`d_iPFPxgVqhz%>kBHsu>$qY?GAXLr4-Bl05PQ!3PN_SyGz<vF}x;_=cHzu$_MF)C9bGo*{-ef1j8kKQDd_!+ST8U)A5&<>B9R@E!O=(y{RkEwW3a|*mipJ1Eqtie_VNcD$6_+c*9hZ_pkD6;jmr=99U$QX5wmO_aw(NI8hp}hD7K|doGaQOR)iX{)rfiYHKQ#ry$o8K>1dw7v6&jeqIeHVq!_%cfHWqq9B+q%l58z6|t)H|&kaT%MEshky`+^|C&kS2Z03BjNS!@u&`C0eD1vHpJIfY?DL)o~&QYsw6{CBlM=ayhXYT(wvGNv%XSn4-H_V{N)<x>Q~!QwN*O16bTHf?4?N%pY7V9N!<h%;$G*Yrk06)t4K$h0cL*)cvrF4j>(cF;+|ApSSPb%zl_?3i#uOJOX*(>Ei+AQBis^8a8$p*3H@e-jJBOPKCJ4;NoT{4_?vfYcbm?hvFwOaW{{b3T5-A?6{%sxxdsa};7iPLc1x_AVd7`we!$>KH&m>xXH<X`cha&RQQq$>LQ)G+c(kYF{P7FP?-!tlDQn@}q>oN!}~Mmg@>Zvj0^=bcQRzC9@{NE540CAsbafmA^;9rlI`7*?u%Y6l+;RF79W+K|mA2h!h7wRaS&TnkxXojaVbX@`@`#jQ(Ik9h|DbntCq6%SD&G+yXvAAJ3=2lN1cXz+1IH{wZTZoW85U`PLS~8rQx+*^_QU**mzvCT&l`3Des^>jhjwuA7m*^Jo3RsG^a;?x;aRO%E`^NU;vWj%%L33j<C<q2A!Y5$OlQoh>dv*okyPy}Kj9Z)HZpf6ntjUvf`EZ@#!do7g_WCy|6e|LkT$gc}t=>oo+z3f!we<$6{^!LsSVpV}(Ii+C46OJ`<6hey~zv*<g*(?f?p(uPz*YqDWL5qcfMbrpiZC0}zwc?g!kRHp;Nl@4Y<;xSV~C?3baTm3S^j;Jp|0R?G700000@X|cO00000VKYhb
""".strip()


def decode_track_coeffs() -> np.ndarray:
    raw = zlib.decompress(base64.b85decode(TRACK_COEFFS_B85))
    return np.frombuffer(raw, dtype=np.complex64).reshape(len(TRACK_NAMES), 181, 2)


def build_tracks() -> dict[str, np.ndarray]:
    coeffs = decode_track_coeffs()
    samples = np.fft.irfft(coeffs, n=FRAME_COUNT, axis=1).astype(np.float32)
    return {name: samples[idx] for idx, name in enumerate(TRACK_NAMES)}


def make_sprite(radius: int, color: tuple[int, int, int], scale: int = 4) -> np.ndarray:
    size = int(np.ceil(radius * 2 + 4))
    hi_size = size * scale
    img = Image.new("RGBA", (hi_size, hi_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    rr = radius * scale
    center = hi_size / 2
    draw.ellipse((center - rr, center - rr, center + rr, center + rr), fill=color + (255,))
    downsampled = img.resize((size, size), Image.Resampling.LANCZOS)
    return np.asarray(downsampled, dtype=np.float32) / 255.0


def build_background() -> np.ndarray:
    bg = np.full((HEIGHT, WIDTH, 3), BACKGROUND_COLOR, dtype=np.uint8)
    for radius in RING_RADII:
        for angle in np.linspace(0.0, 2.0 * np.pi, RING_DOTS, endpoint=False):
            x = int(round(CENTER[0] + radius * np.cos(angle)))
            y = int(round(CENTER[1] + radius * np.sin(angle)))
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                bg[y, x] = DOT_COLOR
    return bg.astype(np.float32) / 255.0


def alpha_blit(canvas: np.ndarray, sprite: np.ndarray, center: np.ndarray) -> None:
    sprite_h, sprite_w = sprite.shape[:2]
    x0 = int(round(float(center[0]) - sprite_w / 2))
    y0 = int(round(float(center[1]) - sprite_h / 2))
    x1 = max(0, x0)
    y1 = max(0, y0)
    x2 = min(WIDTH, x0 + sprite_w)
    y2 = min(HEIGHT, y0 + sprite_h)
    if x1 >= x2 or y1 >= y2:
        return

    sx1 = x1 - x0
    sy1 = y1 - y0
    sx2 = sx1 + (x2 - x1)
    sy2 = sy1 + (y2 - y1)
    patch = sprite[sy1:sy2, sx1:sx2]
    alpha = patch[..., 3:4]
    canvas[y1:y2, x1:x2] = patch[..., :3] * alpha + canvas[y1:y2, x1:x2] * (1.0 - alpha)


TRACKS = build_tracks()
SPRITES = {name: make_sprite(**spec) for name, spec in SPRITE_SPECS.items()}
BACKGROUND = build_background()
DRAW_ORDER = ("small_orange", "purple1", "green", "purple2", "magenta", "gray")


def make_frame(t: float) -> np.ndarray:
    frame_idx = min(int(round(t * FPS)), FRAME_COUNT - 1)
    canvas = BACKGROUND.copy()
    alpha_blit(canvas, SPRITES["big_orange"], CENTER)
    for name in DRAW_ORDER:
        alpha_blit(canvas, SPRITES[name], TRACKS[name][frame_idx])
    return np.clip(np.round(canvas * 255.0), 0, 255).astype(np.uint8)


def main() -> None:
    clip = VideoClip(make_frame, duration=DURATION)
    clip.write_videofile(
        "/app/output.mp4",
        fps=FPS,
        codec="libx264rgb",
        preset="veryslow",
        audio=False,
        ffmpeg_params=["-crf", "0"],
        logger=None,
    )


if __name__ == "__main__":
    main()
