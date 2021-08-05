import datetime

from django.db import models
from urllib.request import urlopen
from urllib.parse import urlencode
from hashlib import sha1
import xml.etree.ElementTree as ET
import random
from api import settings
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
import django.utils.timezone
import uuid
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
    name = models.CharField(max_length=100, unique=True)
    private_meeting_id = models.CharField(max_length=100, unique=True, blank=False, default=uuid.uuid1)
    public_meeting_id = models.CharField(max_length=100, unique=True, blank=False, default=uuid.uuid1)
    meeting_type = models.CharField(max_length=10)
    attendee_password = models.CharField(max_length=50)
    moderator_password = models.CharField(max_length=50)
    welcome = models.CharField(max_length=400, default='welcome')
    dial_number = models.CharField(max_length=12, default=613 - 555 - 1234)
    voice_bridge = models.CharField(max_length=5, validators=[RegexValidator(r'^\d{1,10}$')],
                                    default=70000 + random.randint(0, 9999))
    max_participant = models.IntegerField(default=0, validators=[
        MaxValueValidator(1000),
        MinValueValidator(0)
    ])
    record = models.BooleanField(default=False)
    duration = models.IntegerField(default=60)
    mute_on_start = models.BooleanField(default=True)
    banner_text = models.CharField(max_length=300, blank=True)
    copyright = models.CharField(max_length=100, blank=True)
    moderator_only_message = models.CharField(max_length=300, blank=True)
    logo = models.URLField(blank=True)
    guest_policy = models.CharField(max_length=25, default='ALWAYS_ACCEPT')
    end_when_no_moderator = models.BooleanField(default=False)
    allow_moderator_to_unmute_user = models.BooleanField(default=False)
    webcam_only_for_moderator = models.BooleanField(default=False)
    auto_start_recording = models.BooleanField(default=False)
    allow_start_stop_recording = models.BooleanField(default=True)
    breakout_room = models.BooleanField(default=True)
    parent_meeting_id = models.CharField(max_length=50, default=private_meeting_id)
    free_join = models.BooleanField(default=False)
    breakout_room_enabled = models.BooleanField(default=True)
    breakout_room_private_chat_enabled = models.BooleanField(default=True)
    breakout_room_record = models.BooleanField(default=False)
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
    @classmethod
    def api_call(self, query, call):
        prepared = "%s%s%s" % (call, query, settings.SALT)
        checksum = sha1(prepared.encode('utf-8')).hexdigest()
        result = "%s&checksum=%s" % (query, checksum)
        return result

    def is_running(self):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', self.private_meeting_id),
        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + 'api/' + call + '?' + hashed
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
        url = settings.BBB_API_URL + 'api/' +call + '?' + hashed
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
        url = settings.BBB_API_URL + call + '?' + hashed
        r = parse(urlopen(url).read())
        if r:
            # Create dict of values for easy use in template
            d = {
                'start_time': r.find('startTime').text,
                'end_time': r.find('endTime').text,
                'participant_count': r.find('participantCount').text,
                'moderator_count': r.find('moderatorCount').text,
                'moderator_pw': r.find('moderatorPW').text,
                'attendee_pw': r.find('attendeePW').text,
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
        url = settings.BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            # Create dict of values for easy use in template
            d = []
            r = result[1].findall('meeting')
            for m in r:
                meeting_id = m.find('meetingID').text
                password = m.find('moderatorPW').text
                d.append({
                    'name': meeting_id,
                    'running': m.find('running').text,
                    'moderator_pw': password,
                    'attendee_pw': m.find('attendeePW').text,
                    'info': Meeting.meeting_info(
                        meeting_id,
                        password)
                })
            return d
        # else:
        #     return 'error'

    def start(self):
        call = 'create'
        voicebridge = 70000 + random.randint(0, 9999)
        print(self.private_meeting_id)
        query = urlencode((
            ('name', self.name),
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
            ('copyright', self.copyright),
            ('moderatorOnlyMessage', self.moderator_only_message),
            ('logo', self.logo),
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


        ))
        hashed = self.api_call(query, call)
        url = settings.BBB_API_URL + 'api/' + call + '?' + hashed
        result = parse(urlopen(url).read())
        return result

    @classmethod
    def join_url(cls, meeting_id, name, password, avatar_url, guest, skip_check_audio, skip_check_audio_on_first_join):
        call = 'join'
        query = urlencode((
            ('meetingID', meeting_id),
            ('password', password),
            ('fullName', name),
            ('avatarURL', avatar_url),
            ('guest', guest),
            ('userdata-bbb_ask_for_feedback_on_logout=', 'False'),
            ('userdata-bbb_skip_check_audio=', skip_check_audio),
            # ('userdata-bbb_skip_check_audio_on_first_join=', skip_check_audio_on_first_join),
            ('userdata-bbb_auto_join_audio=', True)

        ))
        hashed = cls.api_call(query, call)
        url = settings.BBB_API_URL + 'api/' +call + '?' + hashed
        return url

    @classmethod
    def is_meeting_running(cls, meeting_id):
        call = 'isMeetingRunning'
        query = urlencode((
            ('meetingID', meeting_id),
        ))
        hashed = cls.api_call(query, call)
        url = settings.BBB_API_URL + 'api/' +call + '?' + hashed
        result = parse(urlopen(url).read())
        if result:
            return result.find('running').text
        else:
            return 'error'


# class map_meeting(models.Model):
#     meeting_id = models.CharField(max_length=100)
#     url_suffix = models.CharField(max_length=25)
#
#     def __str__(self):
#         return self.title

class event_scheduler(models.Model):
    task_id = models.CharField(max_length= 50)
    meeting_id = models.CharField(max_length=25)
    scheduled_time = models.DateTimeField(blank=False)

