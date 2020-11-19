var Frases=new Array()
Frases[0] = "There's no survivors, just the blood scattered all over the place We built our smoked out, loced out in the fuckin' Chevrolet - DJ Paul 1994.";
Frases[1] = "And we came to break the law, tear da club up Ashes to ashes no dust to dust And you can't trust Three 6 Mafia when we tearin' that club up - Lord Infamous 1993.";
Frases[2] = "So what can I say man, for a day man I don't think that I can even go without smoking haze man. - Gangsta Pat 2001.";
var Q = Frases.length;
var numAleatorio=Math.round(Math.random()*(Q-1));
function mostrarFrases() {
document.write(Frases[numAleatorio]);}