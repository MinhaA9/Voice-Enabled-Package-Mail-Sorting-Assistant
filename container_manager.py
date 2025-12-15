class ContainerManager:
    def __init__(self):
        self.containers ={}
    
    def register(self, name, container):
        self.containers[name] = container

    def get(self, name):
        return self.containers.get(name)
    
    def hide_all(self):
        for cntr in self.containers.values():
            cntr.place_forget()
            cntr.pack_forget()

    def dashboard_show(self, name):
        self.hide_all()
        container = self.get(name)
        if container:
            container.pack(fill="both", expand=True, padx=5, pady=5)

    def show(self, name):
        self.hide_all()
        container = self.get(name)
        if(container):
            container.place(relx=0.5, rely=0.5, anchor="center")