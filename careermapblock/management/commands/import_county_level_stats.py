from django.core.management.base import BaseCommand, CommandError
#from data.models import Site,Location,Series,Row
from careermapblock.models import *
import csv, pdb, re

def slugify(val):
    _slugify_strip_re = re.compile(r'[^\w\s-]')
    _slugify_hyphenate_re = re.compile(r'[-\s]+')
    val = unicode(_slugify_strip_re.sub('', val).strip().lower())
    return _slugify_hyphenate_re.sub('_', val)

def get_or_create_stat (county, column, val):
    stat_value = None
    try:
        stat_value = CountyStatValue.objects.get(county__name=county, stat_type__name = column)
    except CountyStatValue.DoesNotExist:
        stat_value = CountyStatValue()
        stat_value.cmap_id = county.cmap_id
        stat_value.county = county
        stat_value.stat_type = column
    print "Setting value of stat %s to %s for county %s" % (column, val, county)
    stat_value.value = val
    stat_value.save()    

class Command(BaseCommand):
    args = ''
    help = ''
    
        
    
    def handle(self, *args, **options):
        path_to_files = 'county_stats'
        county_stat_columns =  os.listdir (path_to_files)
        #(location,created) = Location.objects.get_or_create(name='H1',site=site)
    
        errors = ""
        #TODO: make c.name tolower so lookup will be case-insensitive
        counties = dict([(c.name.lower(), c) for c in County.objects.all()])
        columns = dict([(slugify(c.name), c) for c in CountyStatType.objects.all()])
        
        
        #pdb.set_trace()
        
        for filename in county_stat_columns:
            print filename
            column = filename.replace ('.csv', '')
            #open the file
            reader = csv.reader(open("%s/%s" % (path_to_files, filename)))
            
            if column in columns.keys():
                print "%s found in list of columns" % column
                
                var = raw_input("Replace values for column \"%s\" with the values in file \"%s\" ? (y/n)\n" % ( columns[column].name,  filename))
                if var == 'y':
                    for row in reader:
                        if row[0].lower() in counties.keys():
                            county_obj = counties[row[0].lower()]
                            #pdb.set_trace()
                            column_obj =  columns[column]
                            print "%s found in list of counties" % row[0]
                            get_or_create_stat (county_obj, column_obj, row[1])
                        else:
                            print "%s not found in list of counties " % row[0]
            else:
                print "%s not found in list of columns" % column
                    
                    
            #pdb.set_trace()
            #read in the whole file into a 2D array.
            
            #make a list of counties
            
            #assert the counties exist in the DB
            
            #assert the stats exist in the DB
            
            #prompt the user if they want to replace the values in the DB with the ones in the file
            
            #exit
        
            #(series,created) = Series.objects.get_or_create(name=column,location=location)
            #reader = csv.reader(open("columns/%s.csv" % column))
            #for row in reader:
            #    datetime = row[0]
            #    datum = row[1]
            #    r = Row.objects.create(series=series,
            #                           timestamp=datetime,
            #                           value=datum)

