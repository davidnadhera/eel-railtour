from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.dialects.sqlite import REAL,TIME
from sqlalchemy.ext.associationproxy import association_proxy
from dbutils import get_or_create
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Presun(Base):
    __tablename__ = "presuny"
    od_id = Column(ForeignKey("bod.id"), primary_key=True)
    do_id = Column(ForeignKey("bod.id"), primary_key=True)
    km = Column(REAL)
    cas = Column(Integer)
    od = relationship("Bod", back_populates="presuny_od", foreign_keys=[od_id])
    do = relationship("Bod", back_populates="presuny_do", foreign_keys=[do_id])

class Bod(Base):
    __tablename__ = 'bod'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100))
    lower_name = Column(String(100))
    type = Column(String(20))
    gps_N = Column(REAL)
    gps_E = Column(REAL)
    uzel = Column(Boolean)

    presuny_od = relationship("Presun", back_populates="od", foreign_keys=[Presun.od_id])
    presuny_do = relationship("Presun", back_populates="do", foreign_keys=[Presun.do_id])

    sousede_tam = association_proxy("presuny_od", "do")
    sousede_zpet = association_proxy("presuny_do", "od")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "bod",
    }

    def __repr__(self):
        return f"{self.id!r} {self.name!r}"

class Stanice(Bod):
    cislo = Column(Integer)
    prestup = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "stanice",
    }

class Checkpoint(Bod):
    active = Column(Boolean)
    body = Column(Integer)
    kraj = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "checkpoint",
    }


#
#
#
#     manager = relationship("Manager", back_populates="teams")
#
#     manager_id = Column(Integer, ForeignKey('manager.id'))
#
#     players_selling = relationship("PlayerMarket",
#                                    back_populates="selling_team",
#                                    foreign_keys='PlayerMarket.selling_team_id')
#     players_bought = relationship("PlayerMarket",
#                                   back_populates="buying_team",
#                                   foreign_keys='PlayerMarket.buying_team_id')
#     stats = relationship("TeamStats", back_populates="team")
#
#     @property
#     def url(self):
#         return TEAM_URL.format(id=self.id)
#
#     def __repr__(self):
#         return f"Team(id={self.id!r}, name={self.name!r}, nationality={self.nationality!r})"
#
#     def scrape_team(self, ha_session, stats_date):
#         session = object_session(self)
#         scraper = TeamScraper(ha_session, self.url)
#
#         if manager_id := scraper.manager_id():
#             self.manager = get_or_create(session, Manager, id=manager_id)
#             if not self.manager.name:
#                 self.manager.scrape_manager(ha_session)
#         self.name = scraper.name()
#         league = scraper.league()
#         self.nationality = league.nationality
#         session.commit()
#
#         stats = get_or_create(session, TeamStats, team_id=self.id, date=stats_date)
#         stats.league = league.level
#         stats.rank = scraper.rank()
#         session.commit()
#
#
# class TeamStats(Base):
#     __tablename__ = 'team_stats'
#
#     date = Column(Date, primary_key=True, nullable=False)
#     team_id = Column(Integer, ForeignKey('team.id'), primary_key=True, nullable=False)
#     league = Column(Integer)
#     rank = Column(Integer)
#
#     team = relationship("Team", back_populates="stats")
#
#     def __repr__(self):
#         return f"Team_stats(name={self.team.name!r}, date={self.date!r}, rank={self.rank!r})"
