
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class DockerServer(Base):
    __tablename__ = 'docker_server'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, nullable=False)
    domain = Column(String(128), index=False, nullable=False)
    username = Column(String(128), index=False, nullable=False)
    passwd = Column(String(128), index=False, nullable=False)


class DbAuthUser(Base):
    __tablename__ = 'db_auth_user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String(128), index=False, nullable=False)
    username = Column(String(50), index=True, nullable=False)
    passwd = Column(String(128), index=False, nullable=False)
    status = Column(Integer, index=False, nullable=False)



class DbQAgentServer(Base):
    __tablename__ = 'db_qagent_server'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), index=True, nullable=False)
    host = Column(String(128), index=True, nullable=False, default='localhost')
    port = Column(Integer, index=False, nullable=False, default=6305)
    status = Column(Integer, index=False, nullable=False, default=0)



class DbQAgentContainer(Base):
    __tablename__ = 'db_qagent_container'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    server_id = Column(Integer, index=True, nullable=True)
    container_id = Column(String(128), index=True, nullable=False)
    container_name = Column(String(128), index=True, nullable=False)
    work_path = Column(String(2000), index=False, nullable=True)
    images_id = Column(String(128), index=False, nullable=True)
    names = Column(String(2000), index=False, nullable=True)
    labels = Column(String(3000), index=False, nullable=True)
    ports = Column(String(128), index=True, nullable=True)
    running_for = Column(String(128), index=True, nullable=True)
    state = Column(String(128), index=False, nullable=True)
    status = Column(String(128), index=False, nullable=True)
    size = Column(String(128), index=False, nullable=True)

