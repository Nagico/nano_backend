## 数据库表设计

```plantuml
scale 800 width

map User {
    id=>int
    username=>char
    password=>char
    email=>char
    is_active: 是否激活=>int
    is_superuser: 是否可以管理后台=>int
    data_joined=>datetime
    avatar=>image
    collection_anime: 收藏列表=>many_to_many
    collection_place: 收藏列表=>many_to_many
}

map Anime {
    id=>int
    create_user=>foreign_key
    contributor=>many_to_many
    title=>char
    title_cn=>char
    description=>text
    image=>url
    create_time=>datetime
    update_time=>datetime
    place: 地点列表=>many_to_many
    status: 状态=>int(未发布, 待审核, 审核通过, 审核不通过)
}

map Place {
    id=>int
    create_user=>foreign_key
    contributor=>many_to_many
    name=>char
    address=>char
    description=>text
    latitude=>float
    longitude=>float
    photo=>one_to_many
    status=>int
}

map Photo {
    id=>int
    create_user=>foreign_key
    name=>char
    description=>text
    image=>image
    type=>int(番剧, 现实)
    status=>int
}

User::collection_anime --> Anime::id : list
User::collection_place --> Place::id : list
Anime::place --> Place::id : list
Place::photo --> Photo::id : list

```
