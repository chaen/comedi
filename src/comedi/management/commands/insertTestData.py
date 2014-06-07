from django.core.management.base import NoArgsCommand, make_option
from comedi.models import Client, Seller
from comedi.models import City
from comedi.models import Period
from comedi.models import Family, SubFamily, Tva, Unit, Product
from comedi.models import DepositMode, UsualComment, Order, OrderItem

from random import randint, uniform
import datetime
import time

class Command(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
      
      nb_city = 2
      nb_seller = 5
      nb_client = 10
      nb_family = 3
      nb_sub_family = 10
      nb_product = 50
      nb_order = 200
      max_item_per_order = 5
      

      # create cities
      cities = {}
      for c in range( nb_city ):
        city = City( name = "city_%s" % c, code = "5760%s" % c )
        city.save()
        cities["city_%s" % c] = city

      # create clients
      clients = {}
      for c in range( nb_client ):
        client = Client(first_name = "first_name_%s"%c,
                        last_name = "last_name_%s"%c,
                        nickname = "nickname_%s"%c,
                        phone = "%10d"%c,
                        cellphone = "%10d" % c,
                        email = "%s@comedi.com" % c,
                        comment = "comment client %s" % c,
                        star = randint( 1, 6 ),
                        address = "address client %s" % c,
                        city = cities.values()[randint( 0, nb_city - 1 )]
                        )
        clients["first_name_%s" % c] = client
        client.save()

      # Create sellers
      sellers = {}
      for s in range( nb_seller ):
        seller = Seller( name = "seller_%s" % s )
        sellers[seller.name] = seller
        seller.save()

      # create periods
      periods = {}
      all2013 = Period( name = "all2013", begin_date = "2013-01-01",
                   end_date = "2013-12-31", comment = "All 2013",
                   prefix = "2013_", archived = True )
      periods["all2013"] = all2013
      
      noel2013 = Period( name = "noel2013", begin_date = "2013-12-20",
             end_date = "2013-12-25", comment = "Noel 2013",
             prefix = "noel13_", archived = True )
      periods["noel2013"] = noel2013
      
      all2014 = Period( name = "all2014", begin_date = "2014-01-01",
                   end_date = "2014-12-31", comment = "All 2014",
                   prefix = "2014_", archived = False )
      periods["all2014"] = all2014

      noel2014 = Period( name = "noel2014", begin_date = "2014-12-20",
             end_date = "2014-12-25", comment = "Noel 2014",
             prefix = "noel14_", archived = False )
      periods["noel2014"] = noel2014

      for p in periods.values():
        p.save()
        
      # Create families
      families = {}
      for f in range(nb_family):
        family = Family( name = "family_%s" % f )
        families[family.name] = family
        family.save()

      # Create subFamilies
      subFamilies = {}
      for f in range( nb_sub_family ):
        subFamily = SubFamily( name = "subFamily_%s" % f,
                               family = families.values()[randint( 0, nb_family - 1 )] )

        subFamilies[subFamily.name] = subFamily
        subFamily.save()

      # Create TVA
      tvas = {}
      tva7 = Tva( name = "7%%", rate = 7 )
      tvas[7] = tva7
      tva10 = Tva( name = "10%%", rate = 10 )
      tvas[10] = tva10
      tva20 = Tva( name = "20%%", rate = 20 )
      tvas[20] = tva20

      for t in tvas.values():
        t.save()

      # Create units
      units = {}
      units["unit1"] = Unit( name = "unit1" )
      units["unit2"] = Unit( name = "unit2" )
      units["unit3"] = Unit( name = "unit3" )
      units["unit4"] = Unit( name = "unit4" )
      units["unit5"] = Unit( name = "unit5" )

      for u in units.values():
        u.save()

      # Create product
      products = {}
      for p in range(nb_product):
        product = Product(name = "product_%s"%p,
                          code = "%s"%p,
                          price = p,
                          subFamily = subFamilies.values()[randint(0,nb_sub_family -1)],
                          ttc = randint(0,1),
                          tva = tvas.values()[randint(0,2)],
                          prod_unit = units.values()[randint( 0, 4 )],
                          sell_unit = units.values()[randint( 0, 4 )],
                          locked = randint( 0, 1 ) )
        products[product.name] = product
        product.save()

      deposit = DepositMode( name = "Cheque" )
      deposit.save()

      usualComments = {}
      usualComments["usualComment1"] = UsualComment( comment = "usualComment1" )
      usualComments["usualComment2"] = UsualComment( comment = "usualComment2" )
      usualComments["usualComment3"] = UsualComment( comment = "usualComment3" )

      for u in usualComments.values():
        u.save()

      # Create orders
      orders = {}
      for o in range( nb_order ):
        per = periods.values()[randint(0, len(periods) - 1)]
        print per.begin_date
        sd = datetime.datetime.strptime( per.begin_date, "%Y-%m-%d" ).date()
        ed = datetime.datetime.strptime( per.end_date, "%Y-%m-%d" ).date()
        delta = ed - sd
        pickD = sd + datetime.timedelta( days = randint( 0, delta.days ) )
        orderD = sd + datetime.timedelta( days = randint( -1, delta.days - 1 ) )
        
        order = Order( code = "%s%s"%(per.prefix, o),
                      client = clients.values()[randint(0, nb_client -1)],
                      comment = "Comment %s"%o,
                      deposit = [None, deposit][randint(0,1)],
                      order_date = orderD,
                      pickup_date = pickD,
                      seller = sellers.values()[randint( 0, nb_seller - 1 )],
                      period = per,
                      valid = ([0] + [1] *10)[randint(0,10)],
                      )
        orders[order.code] = order
        order.save()

        print "%s" % order

        for i in range(randint(1,max_item_per_order)):
          orderItem = OrderItem(product = products.values()[randint(0,nb_product -1)],
                                unit = units.values()[randint(0,len(units)-1)],
                                quantity = uniform(1,10),
                                usualComment = ([None] + usualComments.values())[randint(0,len(usualComments))],
                                extraComment = "comment",
                                order = order,
                                prepared = randint( 0, 1 ),
                                modified = randint( 0, 1 ),
                                ordered = randint( 0, 1 ) )
          orderItem.save()
          print "\t%s" % orderItem
