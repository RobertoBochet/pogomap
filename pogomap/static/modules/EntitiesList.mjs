export class EntitiesList extends Array {
    constructor(env) {
        super();
        this.env = env;
    }

    push(...entities) {
        super.push(...entities);

        entities.forEach((entity) => {
            entity.marker.setMap(this.env.gui.map);

            entity.marker.addListener("click", () => {
                this.env.setCurrentEntity(entity);
            });
        });
    }

    remove(...entities) {
        entities.forEach((entity) => {
            let id = typeof entity === "number" ? entity : entity.id;
            this.filter((entity) => {
                return id === entity.id;
            });
            entity.marker.setMap(null);
        });
    }
}
