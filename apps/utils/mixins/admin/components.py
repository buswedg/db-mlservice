from .atoms import CoverSizeImageAdminMixin, BodyAdminMixin, BodyExcerptAdminMixin, \
    PositionAdminMixin, DescriptionAdminMixin, OrderAdminMixin, TitleAdminMixin


class PageAdminMixin(DescriptionAdminMixin):
    list_display = \
        DescriptionAdminMixin.list_display + \
        [

        ]

    fields = \
        DescriptionAdminMixin.fields + \
        [
            'summary',
        ]

    readonly_fields = \
        DescriptionAdminMixin.readonly_fields + \
        [

        ]


class HeroAdminMixin(TitleAdminMixin, CoverSizeImageAdminMixin, BodyAdminMixin, PositionAdminMixin):
    list_display = \
        TitleAdminMixin.list_display + \
        CoverSizeImageAdminMixin.list_display + \
        BodyAdminMixin.list_display + \
        PositionAdminMixin.list_display + \
        [

        ]

    fields = \
        TitleAdminMixin.fields + \
        CoverSizeImageAdminMixin.fields + \
        BodyAdminMixin.fields + \
        PositionAdminMixin.fields + \
        [

        ]

    readonly_fields = \
        TitleAdminMixin.readonly_fields + \
        CoverSizeImageAdminMixin.readonly_fields + \
        BodyAdminMixin.readonly_fields + \
        PositionAdminMixin.readonly_fields + \
        [

        ]


class ContentAdminMixin(OrderAdminMixin, TitleAdminMixin, BodyAdminMixin, PositionAdminMixin):
    list_display = \
        OrderAdminMixin.list_display + \
        TitleAdminMixin.list_display + \
        BodyAdminMixin.list_display + \
        PositionAdminMixin.list_display + \
        [

        ]

    fields = \
        OrderAdminMixin.fields + \
        TitleAdminMixin.fields + \
        BodyAdminMixin.fields + \
        PositionAdminMixin.fields + \
        [

        ]

    readonly_fields = \
        OrderAdminMixin.readonly_fields + \
        TitleAdminMixin.readonly_fields + \
        BodyAdminMixin.readonly_fields + \
        PositionAdminMixin.readonly_fields + \
        [

        ]


class ContentImageAdminMixin(OrderAdminMixin, TitleAdminMixin, CoverSizeImageAdminMixin, BodyAdminMixin,
                             PositionAdminMixin):
    list_display = \
        OrderAdminMixin.list_display + \
        TitleAdminMixin.list_display + \
        CoverSizeImageAdminMixin.list_display + \
        BodyAdminMixin.list_display + \
        PositionAdminMixin.list_display + \
        [

        ]

    fields = \
        OrderAdminMixin.fields + \
        TitleAdminMixin.fields + \
        CoverSizeImageAdminMixin.fields + \
        BodyAdminMixin.fields + \
        PositionAdminMixin.fields + \
        [

        ]

    readonly_fields = \
        OrderAdminMixin.readonly_fields + \
        TitleAdminMixin.readonly_fields + \
        CoverSizeImageAdminMixin.readonly_fields + \
        BodyAdminMixin.readonly_fields + \
        PositionAdminMixin.readonly_fields + \
        [

        ]


class CarouselAdminMixin(OrderAdminMixin, TitleAdminMixin, CoverSizeImageAdminMixin):
    list_display = \
        OrderAdminMixin.list_display + \
        TitleAdminMixin.list_display + \
        CoverSizeImageAdminMixin.list_display + \
        [

        ]

    fields = \
        OrderAdminMixin.fields + \
        TitleAdminMixin.fields + \
        CoverSizeImageAdminMixin.fields + \
        [

        ]

    readonly_fields = \
        OrderAdminMixin.readonly_fields + \
        TitleAdminMixin.readonly_fields + \
        CoverSizeImageAdminMixin.readonly_fields + \
        [

        ]


class FeatureAdminMixin(OrderAdminMixin, TitleAdminMixin, BodyAdminMixin):
    list_display = \
        OrderAdminMixin.list_display + \
        TitleAdminMixin.list_display + \
        BodyAdminMixin.list_display + \
        [
            'featured',
        ]

    fields = \
        OrderAdminMixin.fields + \
        TitleAdminMixin.fields + \
        BodyAdminMixin.fields + \
        [
            'featured',
        ]

    readonly_fields = \
        OrderAdminMixin.readonly_fields + \
        TitleAdminMixin.readonly_fields + \
        BodyAdminMixin.readonly_fields + \
        [

        ]


class DocumentAdminMixin(TitleAdminMixin, BodyAdminMixin):
    list_display = \
        TitleAdminMixin.list_display + \
        BodyAdminMixin.list_display + \
        [
            'datetime',
            'published',
            'featured',
        ]

    fields = \
        TitleAdminMixin.fields + \
        BodyAdminMixin.fields + \
        [
            'datetime',
            'published',
            'featured',
        ]

    readonly_fields = \
        TitleAdminMixin.readonly_fields + \
        BodyAdminMixin.readonly_fields + \
        [

        ]


class PostAdminMixin(TitleAdminMixin, BodyExcerptAdminMixin):
    list_display = \
        TitleAdminMixin.list_display + \
        BodyExcerptAdminMixin.list_display + \
        [
            'datetime',
            'published',
            'featured',
        ]

    fields = \
        TitleAdminMixin.fields + \
        BodyExcerptAdminMixin.fields + \
        [
            'datetime',
            'published',
            'featured',
        ]

    readonly_fields = \
        TitleAdminMixin.readonly_fields + \
        BodyExcerptAdminMixin.readonly_fields + \
        [

        ]
