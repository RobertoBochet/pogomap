from sqlalchemy import Column, String, Table, MetaData, Integer, Boolean, Float

metadata = MetaData()

editor_keys = Table("editorkeys", metadata,
                    Column("key", String(32), primary_key=True),
                    Column("comment", String)
                    )

in_pogo = Table("in_pogo", metadata,
                Column("id", Integer, primary_key=True),
                Column("latitude", Float),
                Column("longitude", Float),
                Column("name", String),
                Column("image", String),
                Column("guid", String),
                Column("type", String),
                Column("is_eligible", Boolean)
                )

not_in_pogo = Table("not_in_pogo", metadata,
                    Column("id", Integer, primary_key=True),
                    Column("latitude", Float),
                    Column("longitude", Float),
                    Column("name", String),
                    Column("image", String),
                    Column("guid", String),
                    Column("is_eligible", Boolean)
                    )

unverified = Table("unverified", metadata,
                   Column("id", Integer, primary_key=True),
                   Column("latitude", Float),
                   Column("longitude", Float),
                   Column("name", String),
                   Column("image", String),
                   Column("guid", String)
                   )

verified = Table("verified", metadata,
                 Column("id", Integer, primary_key=True),
                 Column("latitude", Float),
                 Column("longitude", Float),
                 Column("name", String),
                 Column("image", String),
                 Column("guid", String),
                 Column("type", String),
                 Column("is_eligible", Boolean)
                 )

portals = Table("portals", metadata,
                Column("id", Integer, primary_key=True),
                Column("latitude", Float),
                Column("longitude", Float),
                Column("name", String),
                Column("image", String),
                Column("guid", String)
                )

pokestops = Table("pokestops", metadata,
                  Column("id", Integer, primary_key=True),
                  Column("latitude", Float),
                  Column("longitude", Float),
                  Column("name", String),
                  Column("image", String),
                  Column("guid", String),
                  Column("is_eligible", Boolean)
                  )

pokestops_eligible = Table("pokestops_eligible", metadata,
                           Column("id", Integer, primary_key=True),
                           Column("latitude", Float),
                           Column("longitude", Float),
                           Column("name", String),
                           Column("image", String),
                           Column("guid", String)
                           )

gyms = Table("gyms", metadata,
             Column("id", Integer, primary_key=True),
             Column("latitude", Float),
             Column("longitude", Float),
             Column("name", String),
             Column("image", String),
             Column("guid", String),
             Column("is_eligible", Boolean)
             )

gyms_eligible = Table("gyms_eligible", metadata,
                      Column("id", Integer, primary_key=True),
                      Column("latitude", Float),
                      Column("longitude", Float),
                      Column("name", String),
                      Column("image", String),
                      Column("guid", String)
                      )
