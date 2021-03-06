class TransactionSavePoint(object):
    def __init__(self, session, parent=None, info=None, index=0):
        self.session = session
        self.index = index
        self.child = None
        self.parent = parent
        self.info = info
    
    def find_save_point(self, info):
        if self.info == info:
            return self
        if self.child:
            return self.child.find_save_point(info)
    
    def tail(self):
        if self.child:
            return self.child.tail()
        return self
    
    def unlink(self):
        if self.parent:
            self.parent.child = None

class TransactionSession(object):
    def __init__(self, save_point_class=TransactionSavePoint):
        self.save_point_class = save_point_class
        self.root_save_point = self.save_point_class(session=self, info=None)
        self.actions = list()
    
    def add_save_point(self, info=None):
        tail = self.root_save_point.tail()
        child = self.save_point_class(session=self, parent=tail, info=info, index=len(self.actions))
        tail.child = child
        return child
    
    def pop_save_point(self, info=None):
        if info is None:
            result = self.root_save_point
            result.child = None
        else:
            result = self.root_save_point.find_save_point(info)
            result.unlink()
        actions = self.actions[result.index:]
        self.actions = self.actions[:result.index]
        return actions
    
    def tail(self):
        return self.root_save_point.tail()
    
    def record_action(self, action):
        self.actions.append(action)
