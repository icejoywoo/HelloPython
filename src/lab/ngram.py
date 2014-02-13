#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-9
# http://blog.jobbole.com/54707/


class NGram(object):
    def __init__(self, text, n=3):
        self.length = None
        self.n = n
        self.table = {}
        self.parse_text(text)
        self.calculate_length()
 
    def parse_text(self, text):
        chars = ' ' * self.n  # initial sequence of spaces with length n

        for letter in (" ".join(text.split()) + " "):
            chars = chars[1:] + letter  # append letter to sequence of length n
            self.table[chars] = self.table.get(chars, 0) + 1  # increment count

    def calculate_length(self):
        """ Treat the N-Gram table as a vector and return its scalar magnitude
        to be used for performing a vector-based search.
        """
        self.length = sum([x * x for x in self.table.values()]) ** 0.5
        return self.length
 
    def __sub__(self, other):
        """ Find the difference between two NGram objects by finding the cosine
        of the angle between the two vector representations of the table of
        N-Grams. Return a float value between 0 and 1 where 0 indicates that
        the two NGrams are exactly the same.
        """
        if not isinstance(other, NGram):
            raise TypeError("Can't compare NGram with non-NGram object.")
 
        if self.n != other.n:
            raise TypeError("Can't compare NGram objects of different size.")
 
        total = 0
        for k in self.table:
            total += self.table[k] * other.table.get(k, 0)
 
        return 1.0 - (float(total)) / (float(self.length) * float(other.length))
 
    def find_match(self, languages):
        """ Out of a list of NGrams that represent individual languages, return
        the best match.
        """
        return min(languages, lambda n: self - n)

if __name__ == "__main__":
    english = NGram("""My dear Alicia,--You are very good in taking notice of Frederica, and
I am grateful for it as a mark of your friendship; but as I cannot have
any doubt of the warmth of your affection, I am far from exacting so
heavy a sacrifice. She is a stupid girl, and has nothing to recommend
her. I would not, therefore, on my account, have you encumber one moment
of your precious time by sending for her to Edward Street, especially
as every visit is so much deducted from the grand affair of education,
which I really wish to have attended to while she remains at Miss
Summers's. I want her to play and sing with some portion of taste and
a good deal of assurance, as she has my hand and arm and a tolerable
voice. I was so much indulged in my infant years that I was never
obliged to attend to anything, and consequently am without the
accomplishments which are now necessary to finish a pretty woman. Not
that I am an advocate for the prevailing fashion of acquiring a perfect
knowledge of all languages, arts, and sciences. It is throwing time
away to be mistress of French, Italian, and German: music, singing,
and drawing, &c., will gain a woman some applause, but will not add
one lover to her list--grace and manner, after all, are of the greatest
importance. I do not mean, therefore, that Frederica's acquirements
should be more than superficial, and I flatter myself that she will not
remain long enough at school to understand anything thoroughly. I hope
to see her the wife of Sir James within a twelvemonth. You know on what
I ground my hope, and it is certainly a good foundation, for school must
be very humiliating to a girl of Frederica's age. And, by-the-by, you
had better not invite her any more on that account, as I wish her to
find her situation as unpleasant as possible. I am sure of Sir James at
any time, and could make him renew his application by a line. I shall
trouble you meanwhile to prevent his forming any other attachment when
he comes to town. Ask him to your house occasionally, and talk to him of
Frederica, that he may not forget her. Upon the whole, I commend my own
conduct in this affair extremely, and regard it as a very happy instance
of circumspection and tenderness. Some mothers would have insisted on
their daughter's accepting so good an offer on the first overture; but I
could not reconcile it to myself to force Frederica into a marriage from
which her heart revolted, and instead of adopting so harsh a measure
merely propose to make it her own choice, by rendering her thoroughly
uncomfortable till she does accept him--but enough of this tiresome
girl. You may well wonder how I contrive to pass my time here, and for
the first week it was insufferably dull. Now, however, we begin to mend,
our party is enlarged by Mrs. Vernon's brother, a handsome young man,
who promises me some amusement. There is something about him which
rather interests me, a sort of sauciness and familiarity which I shall
teach him to correct. He is lively, and seems clever, and when I have
inspired him with greater respect for me than his sister's kind offices
have implanted, he may be an agreeable flirt. There is exquisite
pleasure in subduing an insolent spirit, in making a person
predetermined to dislike acknowledge one's superiority. I have
disconcerted him already by my calm reserve, and it shall be my
endeavour to humble the pride of these self important De Courcys still
lower, to convince Mrs. Vernon that her sisterly cautions have been
bestowed in vain, and to persuade Reginald that she has scandalously
belied me. This project will serve at least to amuse me, and prevent
my feeling so acutely this dreadful separation from you and all whom I
love.
""", n=3)
    french = NGram("""Lucie, étudiante des États-Unis, vient d'arriver à Charles de Gaulle, l'aéroport qui accueille chaque jour à Paris, 1 million de visiteurs. Paris. Enfin. Ça a toujours été le rêve de Lucie : vivre dans la Ville lumière, la ville des beaux arts, du quartier latin, du vin, et qui sait, peut-être la ville d'une petite histoire d'amour.
Son projet est d'étudier en France pendant un an, pour obtenir sa licence ès informatique à l'Université de Versailles à St. Quentin-en-Yvelines. C'est l'université qui lui a offert une bourse pour faire ses études. En plus, sa copine Josephine fait ses études là-bas, et Lucie va pouvoir vivre avec elle dans son petit appartement.
Elle prend le RER qui la mène directement à la Gare St. Lazare, en centre-ville. Une fois arrivée, elle cherche le quai du train pour Versailles. Elle monte dans le train, et bientôt il entre dans un tunnel sombre en direction de Versailles. Lucie est un peu déçue, parce qu'elle doit rester à Versailles bien qu'elle veuille vivre à Paris. Mais elle se dit que Versailles n'est qu'à quelques minutes en train de la grande ville de Paris, et qu'il y a aussi plusieurs attractions à Versailles.
Le train sort du tunnel, et en passant par la grande ville, elle voit un grand cimetière, la tour Eiffel et Montmarte avec la basilique du Sacré-Coeur tout près. Quelques instants plus tard, elle arrive en gare de Versailles.
Elle est arrivée à destination. Devant elle le grand Château de Versailles où Louis XIV, le Roi Soleil, organisa des fêtes et vécut la grande vie entouré de ses maîtresses. À droite se trouve l'avenue de St.-Cloud, où est situé l'appartement dans lequel elle va vivre avec Josephine. Fatiguée, mais joyeuse, elle commence à chercher l'adresse de l'appartement. « Toute seule dans un nouveau pays, ne connaissant personne, l'avenir, je t'embrasse vivement ! » se dit Lucie.""", n=3)

    print NGram("Hello, World!", n=3).find_match([english, french])