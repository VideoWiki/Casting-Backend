from django.db import models
from urllib.request import urlopen
from urllib.parse import urlencode
from hashlib import sha1
import xml.etree.ElementTree as ET
import random
from api import settings
from django.core.validators import MaxValueValidator, MinValueValidator
import django.utils.timezone
from api.global_variable import SALT, BBB_API_URL
# Create your models here.

def parse(response):
    try:
        xml = ET.XML(response)
        code = xml.find('returncode').text
        if code == 'SUCCESS':
            return xml
        else:
            raise
    except:
        return None

# todo add meeting type
class Meeting(models.Model):
    user_id = models.IntegerField(blank=False)
    event_name = models.CharField(max_length=100, unique=True)
    event_creator_name = models.CharField(max_length=50)
    event_creator_email = models.CharField(max_length=50)
    private_meeting_id = models.CharField(max_length=100, unique=True)
    public_meeting_id = models.CharField(max_length=100, unique=True)
    meeting_type = models.CharField(max_length=10)
    attendee_password = models.CharField(max_length=50)
    moderator_password = models.CharField(max_length=50)
    welcome = models.CharField(max_length=400, default='welcome')
    description = models.CharField(max_length=300)
    short_description = models.CharField(max_length=150)
    max_participant = models.IntegerField(default=0, validators=[
        MaxValueValidator(1000),
        MinValueValidator(0)
    ])
    record = models.BooleanField(default=False)
    duration = models.IntegerField(default=60)
    mute_on_start = models.BooleanField(default=True)
    banner_text = models.CharField(max_length=300, blank=True)
    logo = models.ImageField(blank=True, upload_to='logo_images')
    guest_policy = models.CharField(max_length=25, default='ALWAYS_ACCEPT')
    end_when_no_moderator = models.BooleanField(default=False)
    allow_moderator_to_unmute_user = models.BooleanField(default=False)
    webcam_only_for_moderator = models.BooleanField(default=False)
    auto_start_recording = models.BooleanField(default=False)
    allow_start_stop_recording = models.BooleanField(default=True)
    disable_cam = models.BooleanField(default=False)
    disable_mic = models.BooleanField(default=False)
    disable_private_chat = models.BooleanField(default=False)
    disable_public_chat = models.BooleanField(default=False)
    disable_note = models.BooleanField(default=False)
    logout_url = models.URLField(blank=True)
    lock_layout = models.BooleanField(default=False)
    lock_on_join = models.BooleanField(default=True)
    hide_users = models.BooleanField(default=False)
    schedule_time = models.DateTimeField(blank=False, default=django.utils.timezone.now)
    moderators = models.EmailField(blank=True)
    primary_color = models.CharField(blank=True, max_length=20)
    secondary_color = models.CharField(blank=True, max_length=20)
    back_image = models.URLField(blank=True)
    event_tag = models.CharField(blank=True, max_length=25)
    schedular_name_reminder = models.CharField(max_length=50)
    cover_image = models.ImageField(blank=True, upload_to='cover_images')
    is_streaming = models.BooleanField(default=False)
    bbb_resolution = models.CharField(max_length=20, default="1280x720")
    bbb_stream_url_facebook = models.URLField(blank=True)
    bbb_stream_url_youtube = models.URLField(blank=True)


    @classmethod
    def api_call(self, query, call):
        prepared = "%s%s%s" % (call, query, SALT)
        checksum = sha1(prepared.encode('utf-8')).hexdigest()
        result = "%s&checksum=%s" % (query, checksum)
        return result

    def is_running(self):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', self.private_meeting_id),
        ))
        hashed = self.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result.find('running').text

    @classmethod
    def end_meeting(cls, private_meeting_id, password):
        call = 'end'
        query = urlencode((
            ('meetingID', private_meeting_id),
            ('password', password),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' +call + '?' + hashed
        result = parse(urlopen(url).read())
        return result

    @classmethod
    def meeting_info(cls, private_meeting_id, password):
        call = 'getMeetingInfo'
        query = urlencode((
            ('meetingID', private_meeting_id),
            ('password', password),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        r = parse(urlopen(url).read())
        if r:
            # Create dict of values for easy use in template
            d = {
                'start_time': r.find('startTime').text,
                'end_time': r.find('endTime').text,
                'participant_count': r.find('participantCount').text,
                'moderator_count': r.find('moderatorCount').text,
                'max_users': r.find('maxUsers').text
            }
            return d
        else:
            return None

    @classmethod
    def get_meetings(cls):
        call = 'getMeetings'
        query = urlencode((
            ('random', 'random'),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            # Create dict of values for easy use in template
            d = []
            r = result[1].findall('meeting')
            for m in r:
                name = m.find('meetingName').text
                password = m.find('moderatorPW').text
                meeting_id = m.find('meetingID').text
                d.append({
                    'name': name,
                    'running': m.find('running').text,
                    'info': Meeting.meeting_info(
                        meeting_id,
                        password)
                })
            return d


    def start(self):
        call = 'create'
        voicebridge = 70000 + random.randint(0, 9999)
        query = urlencode((
            ('name', self.event_name),
            ('meetingID', self.private_meeting_id),
            ('attendeePW', self.attendee_password),
            ('moderatorPW', self.moderator_password),
            ('voiceBridge', voicebridge),
            ('welcome', self.welcome),
            ('maxParticipants', self.max_participant),
            ('record', self.record),
            ('duration', self.duration),
            ('logoutURL', self.logout_url),
            ('muteOnStart', self.mute_on_start),
            ('bannerText', self.banner_text),
            ('logo', str(path_getter(self.logo))),
            ('endWhenNoModerator', self.end_when_no_moderator),
            ('guestPolicy', self.guest_policy),
            ('allowModsToUnmuteUsers', self.allow_moderator_to_unmute_user),
            ('webcamsOnlyForModerator', self.webcam_only_for_moderator),
            ('autoStartRecording', self.auto_start_recording),
            ('allowStartStopRecording', self.allow_start_stop_recording),
            ('lockSettingsDisableCam', self.disable_cam),
            ('lockSettingsDisableMic', self.disable_mic),
            ('lockSettingsDisableNote', self.disable_note),
            ('lockSettingsDisablePrivateChat', self.disable_public_chat),
            ('lockSettingsDisablePublicChat', self.disable_private_chat),
            ('lockSettingsLockedLayout', self.lock_layout),
            ('lockSettingsLockOnJoin', self.lock_on_join),
            ('lockSettingsHideUserList', self.hide_users),
            ('meta_bbb-origin', 'Greenlight'),
            ('meta_bbb-origin-version', "v2"),
            ('meta_bbb-origin-server-name', 'class.video.wiki'),
            ('meta_primary-color', self.primary_color),
            ('meta_secondary-color', self.secondary_color),
            ('meta_back-image', self.back_image),
            ('meta_gl-listed', False)



        ))
        hashed = self.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result

    @classmethod
    def join_url(cls, meeting_id, name, password, avatar_url):
        call = 'join'
        query = urlencode((
            ('meetingID', meeting_id),
            ('password', password),
            ('fullName', name),
            ('avatarURL', avatar_url),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' +call + '?' + hashed
        print(url)
        return url

    @classmethod
    def get_recordings(cls, private_meeting_id):
        call = "getRecordings"
        query = urlencode((
            ('meetingID', private_meeting_id),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        d = []
        r = result[1].findall('recording')
        for m in r:
            a = m.findall("playback")
            for i in a:
                a = i.findall("format")
                for i in a:
                    url = i.find("url").text
                    return url
        return None

    @classmethod
    def is_meeting_running(cls, private_meeting_id):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', private_meeting_id),
        ))
        hashed = cls.api_call(query, call)
        url = BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result.find('running').text


class TemporaryFiles(models.Model):
    created_at = models.DateTimeField(default=django.utils.timezone.now, null=True, blank=True)
    temp_file = models.FileField(upload_to="temporary/%Y/%m/%d")


def path_getter(path):
    url = path.url
    print(path, url, "000")
    return url








