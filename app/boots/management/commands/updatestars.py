from django.core.management.base import NoArgsCommand

from boots.models import Boot


class Command(NoArgsCommand):

    def handle_noargs(self, *args, **options):
        print 'Updating star counts...'

        for boot in Boot.objects.all():
            print ' - ' + unicode(boot)
            boot.update_star_count()

        print 'Finished.'
