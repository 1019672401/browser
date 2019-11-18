# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class CbiCompetition(db.Model):
    __tablename__ = 'cbi_competition'

    competition_no = db.Column(db.Integer, primary_key=True)
    competition_name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    competition_type = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=0, server_default=db.FetchedValue())

    def __repr__(self):
        return "<CbiCompetition(competition_no='%s', competition_name='%s', start_date='%s',end_date='%s'," \
               "competition_type='%s',is_active='%s')>" % (
                   self.competition_no, self.competition_name, self.start_date, self.end_date, self.competition_type,
                   self.is_active)


class CbiEvent(db.Model):
    __tablename__ = 'cbi_event'

    competition_no = db.Column(db.ForeignKey('cbi_competition.competition_no', ondelete='CASCADE'), primary_key=True,
                               nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_name = db.Column(db.String, nullable=False)
    event_type_no = db.Column(db.ForeignKey('cbi_event_type.type_no', ondelete='CASCADE'), nullable=False, index=True)
    track_num = db.Column(db.Integer, nullable=False)
    timeout_time = db.Column(db.Integer, nullable=False)
    timeout_time_bak = db.Column(db.Integer)
    first_score = db.Column(db.Float, nullable=False)
    last_score = db.Column(db.Float, nullable=False)
    is_end = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    cbi_competition = db.relationship('CbiCompetition',
                                      primaryjoin='CbiEvent.competition_no == CbiCompetition.competition_no',
                                      backref=db.backref('cbi_events', cascade="all, delete-orphan"))
    cbi_event_type = db.relationship('CbiEventType', primaryjoin='CbiEvent.event_type_no == CbiEventType.type_no',
                                     backref='cbi_events')


class CbiEventType(db.Model):
    __tablename__ = 'cbi_event_type'

    type_no = db.Column(db.Integer, primary_key=True)
    type_desc = db.Column(db.String, nullable=False)


class CbiMatch(db.Model):
    __tablename__ = 'cbi_match'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no'], ['cbi_event.competition_no', 'cbi_event.event_no'],
                                ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    match_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_type_no = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)
    m_state = db.Column(db.Integer, nullable=False)

    cbi_event = db.relationship('CbiEvent',
                                primaryjoin='and_(CbiMatch.competition_no == CbiEvent.competition_no, CbiMatch.event_no == CbiEvent.event_no)',
                                backref=db.backref('cbi_matches', cascade="all, delete-orphan"))


class CbiRefereePoint(db.Model):
    __tablename__ = 'cbi_referee_point'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no'], ['cbi_event.competition_no', 'cbi_event.event_no'],
                                ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    referee_point_no = db.Column(db.Integer, primary_key=True, nullable=False)

    cbi_event = db.relationship('CbiEvent',
                                primaryjoin='and_(CbiRefereePoint.competition_no == CbiEvent.competition_no, CbiRefereePoint.event_no == CbiEvent.event_no)',
                                backref=db.backref('cbi_referee_points', cascade="all, delete-orphan"))


class CbiRefereeRule(db.Model):
    __tablename__ = 'cbi_referee_rule'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'referee_point_no'],
                                ['cbi_referee_point.competition_no', 'cbi_referee_point.event_no',
                                 'cbi_referee_point.referee_point_no'], ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    referee_point_no = db.Column(db.Integer, primary_key=True, nullable=False)
    evaluate_no = db.Column(db.Integer, primary_key=True, nullable=False)
    evaluate_description = db.Column(db.String, nullable=False)
    evaluate_value = db.Column(db.Float, nullable=False)
    evaluate_type = db.Column(db.Integer, nullable=False)

    cbi_referee_point = db.relationship('CbiRefereePoint',
                                        primaryjoin='and_(CbiRefereeRule.competition_no == CbiRefereePoint.competition_no, CbiRefereeRule.event_no == CbiRefereePoint.event_no, CbiRefereeRule.referee_point_no == CbiRefereePoint.referee_point_no)',
                                        backref=db.backref('cbi_referee_rules', cascade="all, delete-orphan"))


class MtDevice(db.Model):
    __tablename__ = 'mt_device'

    device_no = db.Column(db.Integer, primary_key=True)
    port_used_num = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    pc_ip = db.Column(db.String)


class MtMatchTrack(db.Model):
    __tablename__ = 'mt_match_track'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'match_no'],
                                ['cbi_match.competition_no', 'cbi_match.event_no', 'cbi_match.match_no'],
                                ondelete='CASCADE'),
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'track_no'],
                                ['mt_track_port.competition_no', 'mt_track_port.event_no', 'mt_track_port.track_no'],
                                ondelete='CASCADE'),
        db.Index('trck', 'competition_no', 'event_no', 'track_no')
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    match_no = db.Column(db.Integer, primary_key=True, nullable=False)
    track_no = db.Column(db.Integer, primary_key=True, nullable=False)
    device_no = db.Column(db.Integer, nullable=False)
    port_no = db.Column(db.Integer, nullable=False)
    port_no_bak = db.Column(db.Integer)
    player_or_team_no = db.Column(db.String(10))

    cbi_match = db.relationship('CbiMatch',
                                primaryjoin='and_(MtMatchTrack.competition_no == CbiMatch.competition_no, MtMatchTrack.event_no == CbiMatch.event_no, MtMatchTrack.match_no == CbiMatch.match_no)',
                                backref=db.backref('mt_match_tracks', cascade="all, delete-orphan"))
    mt_track_port = db.relationship('MtTrackPort',
                                    primaryjoin='and_(MtMatchTrack.competition_no == MtTrackPort.competition_no, MtMatchTrack.event_no == MtTrackPort.event_no, MtMatchTrack.track_no == MtTrackPort.track_no)',
                                    backref=db.backref('mt_match_tracks', cascade="all, delete-orphan"))


class MtOriginalScore(db.Model):
    __tablename__ = 'mt_original_score'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'track_no', 'match_no'],
                                ['mt_match_track.competition_no', 'mt_match_track.event_no', 'mt_match_track.track_no',
                                 'mt_match_track.match_no'], ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    track_no = db.Column(db.Integer, primary_key=True, nullable=False)
    match_no = db.Column(db.Integer, primary_key=True, nullable=False)
    original_duration = db.Column(db.Float)
    write_in_time = db.Column(db.DateTime)
    original_duration_second = db.Column(db.Float)
    penalty_time_subtotal = db.Column(db.Integer, server_default=db.FetchedValue())
    penalty_score_subtotal = db.Column(db.Float, server_default=db.FetchedValue())
    penalty_cancel_subtotal = db.Column(db.Integer, server_default=db.FetchedValue())
    original_duration_bak = db.Column(db.Float)
    penalty_time_subtotal_bak = db.Column(db.Integer)
    penalty_score_suntotal_bak = db.Column(db.Integer)
    penalty_cancel_subtotal_bak = db.Column(db.Integer)
    original_duration_second_bak = db.Column(db.Float)


class MtOriginalEvaluate(db.Model):
    __tablename__ = 'mt_original_evaluate'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'track_no', 'match_no'],
                                ['mt_match_track.competition_no', 'mt_match_track.event_no', 'mt_match_track.track_no',
                                 'mt_match_track.match_no'], ondelete='CASCADE'),
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'track_no', 'referee_point_no'],
                                ['ump_referee_allocate.competition_no', 'ump_referee_allocate.event_no',
                                 'ump_referee_allocate.track_no', 'ump_referee_allocate.referee_point_no'],
                                ondelete='CASCADE'),
        db.Index('refe1', 'competition_no', 'event_no', 'track_no', 'referee_point_no')
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    track_no = db.Column(db.Integer, primary_key=True, nullable=False)
    match_no = db.Column(db.Integer, primary_key=True, nullable=False)
    referee_point_no = db.Column(db.Integer, primary_key=True, nullable=False)
    evaluate_no = db.Column(db.Integer, primary_key=True, nullable=False)
    evaluate_value_subtotal = db.Column(db.Float, nullable=False)
    evaluate_moment = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    mt_match_track = db.relationship('MtMatchTrack',
                                     primaryjoin='and_(MtOriginalEvaluate.competition_no == MtMatchTrack.competition_no, MtOriginalEvaluate.event_no == MtMatchTrack.event_no, MtOriginalEvaluate.track_no == MtMatchTrack.track_no, MtOriginalEvaluate.match_no == MtMatchTrack.match_no)',
                                     backref=db.backref('mt_original_evaluates', cascade="all, delete-orphan"))
    ump_referee_allocate = db.relationship('UmpRefereeAllocate',
                                           primaryjoin='and_(MtOriginalEvaluate.competition_no == UmpRefereeAllocate.competition_no, MtOriginalEvaluate.event_no == UmpRefereeAllocate.event_no, MtOriginalEvaluate.track_no == UmpRefereeAllocate.track_no, MtOriginalEvaluate.referee_point_no == UmpRefereeAllocate.referee_point_no)',
                                           backref=db.backref('mt_original_evaluates', cascade="all, delete-orphan"))


class MtTrackPort(db.Model):
    __tablename__ = 'mt_track_port'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no'], ['cbi_event.competition_no', 'cbi_event.event_no'],
                                ondelete='CASCADE'),
        db.Index('dev_port', 'port_no', 'device_no')
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    track_no = db.Column(db.Integer, primary_key=True, nullable=False)
    device_no = db.Column(db.ForeignKey('mt_device.device_no', ondelete='CASCADE'), index=True)
    port_no = db.Column(db.Integer)
    port_no_bak = db.Column(db.Integer)

    cbi_event = db.relationship('CbiEvent',
                                primaryjoin='and_(MtTrackPort.competition_no == CbiEvent.competition_no, MtTrackPort.event_no == CbiEvent.event_no)',
                                backref=db.backref('mt_track_ports', cascade="all, delete-orphan"))
    mt_device = db.relationship('MtDevice', primaryjoin='MtTrackPort.device_no == MtDevice.device_no',
                                backref=db.backref('mt_track_ports', cascade="all, delete-orphan"))


class PrjScreen(db.Model):
    __tablename__ = 'prj_screen'

    screen_no = db.Column(db.Integer, primary_key=True)
    screen_ip = db.Column(db.String, nullable=False)
    screen_content = db.Column(db.String)
    parameter = db.Column(db.String)


class PscoPlayer(db.Model):
    __tablename__ = 'psco_player'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'team_no'], ['tsco_team.competition_no', 'tsco_team.team_no'],
                                ondelete='CASCADE'),
        db.Index('team1', 'competition_no', 'team_no')
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    team_no = db.Column(db.String(10), nullable=False)
    player_no = db.Column(db.String(10), primary_key=True, nullable=False)
    id_no = db.Column(db.String)
    phone_no = db.Column(db.String)
    player_name = db.Column(db.String, nullable=False)
    player_desc = db.Column(db.String, nullable=False)

    tsco_team = db.relationship('TscoTeam',
                                primaryjoin='and_(PscoPlayer.competition_no == TscoTeam.competition_no, PscoPlayer.team_no == TscoTeam.team_no)',
                                backref=db.backref('psco_players', cascade="all, delete-orphan"))


class PscoPlayerTotalScore(db.Model):
    __tablename__ = 'psco_player_total_score'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'player_no'],
                                ['psco_player.competition_no', 'psco_player.player_no'], ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    player_no = db.Column(db.String(10), primary_key=True, nullable=False)
    player_event_total_score = db.Column(db.Float, nullable=False)
    player_total_score = db.Column(db.Float)


class PscoPlayerEventScore(db.Model):
    __tablename__ = 'psco_player_event_score'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no'], ['cbi_event.competition_no', 'cbi_event.event_no'],
                                ondelete='CASCADE'),
        db.ForeignKeyConstraint(['competition_no', 'player_no'],
                                ['psco_player.competition_no', 'psco_player.player_no'], ondelete='CASCADE'),
        db.Index('event2', 'competition_no', 'event_no')
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    player_no = db.Column(db.String(10), primary_key=True, nullable=False)
    event_evaluate_time = db.Column(db.Float)
    event_original_duration = db.Column(db.Float)
    event_score = db.Column(db.Float)
    is_schedule = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_cancel = db.Column(db.Integer)

    cbi_event = db.relationship('CbiEvent',
                                primaryjoin='and_(PscoPlayerEventScore.competition_no == CbiEvent.competition_no, PscoPlayerEventScore.event_no == CbiEvent.event_no)',
                                backref=db.backref('psco_player_event_scores', cascade="all, delete-orphan"))
    psco_player = db.relationship('PscoPlayer',
                                  primaryjoin='and_(PscoPlayerEventScore.competition_no == PscoPlayer.competition_no, PscoPlayerEventScore.player_no == PscoPlayer.player_no)',
                                  backref=db.backref('psco_player_event_scores', cascade="all, delete-orphan"))


class TscoTeam(db.Model):
    __tablename__ = 'tsco_team'

    competition_no = db.Column(db.ForeignKey('cbi_competition.competition_no', ondelete='CASCADE'), primary_key=True,
                               nullable=False)
    team_no = db.Column(db.String(10), primary_key=True, nullable=False)
    team_name = db.Column(db.String, nullable=False)
    leader_name = db.Column(db.String)
    coach_name = db.Column(db.String)
    leader_phone_no = db.Column(db.String)

    cbi_competition = db.relationship('CbiCompetition',
                                      primaryjoin='TscoTeam.competition_no == CbiCompetition.competition_no',
                                      backref=db.backref('tsco_teams', cascade="all, delete-orphan"))


class TscoTeamTotalScore(db.Model):
    __tablename__ = 'tsco_team_total_score'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'team_no'], ['tsco_team.competition_no', 'tsco_team.team_no'],
                                ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    team_no = db.Column(db.String(10), primary_key=True, nullable=False)
    team_event_total_score = db.Column(db.Float, nullable=False)
    team_total_score = db.Column(db.Float)


class TscoTeamEventScore(db.Model):
    __tablename__ = 'tsco_team_event_score'
    __table_args__ = (
        db.ForeignKeyConstraint(['competiton_no', 'event_no'], ['cbi_event.competition_no', 'cbi_event.event_no'],
                                ondelete='CASCADE'),
        db.ForeignKeyConstraint(['competiton_no', 'team_no'], ['tsco_team.competition_no', 'tsco_team.team_no'],
                                ondelete='CASCADE'),
        db.Index('event1', 'competiton_no', 'event_no')
    )

    competiton_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    team_no = db.Column(db.String(10), primary_key=True, nullable=False)
    event_original_duration = db.Column(db.Float)
    event_evaluate_time = db.Column(db.Float)
    event_score = db.Column(db.Float)
    event_original_duration_bak = db.Column(db.Float)
    adjust_score = db.Column(db.Integer)
    is_schedule = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    is_cancel = db.Column(db.Integer)

    cbi_event = db.relationship('CbiEvent',
                                primaryjoin='and_(TscoTeamEventScore.competiton_no == CbiEvent.competition_no, TscoTeamEventScore.event_no == CbiEvent.event_no)',
                                backref=db.backref('tsco_team_event_scores', cascade="all, delete-orphan"))
    tsco_team = db.relationship('TscoTeam',
                                primaryjoin='and_(TscoTeamEventScore.competiton_no == TscoTeam.competition_no, TscoTeamEventScore.team_no == TscoTeam.team_no)',
                                backref=db.backref('tsco_team_event_scores', cascade="all, delete-orphan"))


class UmpRefereeAllocate(db.Model):
    __tablename__ = 'ump_referee_allocate'
    __table_args__ = (
        db.ForeignKeyConstraint(['competition_no', 'event_no', 'track_no'],
                                ['mt_track_port.competition_no', 'mt_track_port.event_no', 'mt_track_port.track_no'],
                                ondelete='CASCADE'),
    )

    competition_no = db.Column(db.Integer, primary_key=True, nullable=False)
    event_no = db.Column(db.Integer, primary_key=True, nullable=False)
    track_no = db.Column(db.Integer, primary_key=True, nullable=False)
    referee_point_no = db.Column(db.Integer, primary_key=True, nullable=False)
    referee_no = db.Column(db.String(10))
    referee_name = db.Column(db.String)
    referee_phone = db.Column(db.String)
    referee_id_no = db.Column(db.String)
    referee_password = db.Column(db.String)

    mt_track_port = db.relationship('MtTrackPort',
                                    primaryjoin='and_(UmpRefereeAllocate.competition_no == MtTrackPort.competition_no, UmpRefereeAllocate.event_no == MtTrackPort.event_no, UmpRefereeAllocate.track_no == MtTrackPort.track_no)',
                                    backref=db.backref('ump_referee_allocates', cascade="all, delete-orphan"))
