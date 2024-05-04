class TimeStampAdminMixin:
    list_display = \
        [
            'created_at',
            'modified_at',
        ]

    fields = \
        [
            'created_at',
            'modified_at',
        ]

    readonly_fields = \
        [
            'created_at',
            'modified_at',
        ]


class UuidAdminMixin:
    list_display = \
        [

        ]

    fields = \
        [
            'uuid',
        ]

    readonly_fields = \
        [
            'uuid',
        ]


class OrderAdminMixin:
    list_display = \
        [
            'order',
        ]

    fields = \
        [
            'order',
        ]

    readonly_fields = [

    ]


class TitleAdminMixin:
    list_display = \
        [
            'title',
        ]

    fields = \
        [
            'title',
        ]

    readonly_fields = \
        [

        ]


class TitleSlugAdminMixin:
    list_display = \
        [
            'title',
        ]

    fields = \
        [
            'title',
            'slug',
        ]

    readonly_fields = \
        [
            'slug',
        ]


class DescriptionAdminMixin:
    list_display = \
        [

        ]

    fields = \
        [
            'description',
        ]

    readonly_fields = \
        [

        ]


class BodyAdminMixin:
    list_display = \
        [

        ]

    fields = \
        [
            'body',
        ]

    readonly_fields = \
        [

        ]


class BodyExcerptAdminMixin:
    list_display = \
        [

        ]

    fields = \
        [
            'body',
            'excerpt_short',
            'excerpt_long',
        ]

    readonly_fields = \
        [

        ]


class PositionAdminMixin:
    list_display = \
        [
            'position',
        ]

    fields = \
        [
            'position',
        ]

    readonly_fields = \
        [

        ]


class LogoSizeImageAdminMixin:
    list_display = \
        [
            'image',
            'alt',
        ]

    fields = \
        [
            'image',
            'image_xs',
            'image_md',
            'alt',
        ]

    readonly_fields = \
        [
            'image_xs',
            'image_md',
        ]


class CoverSizeImageAdminMixin:
    list_display = \
        [
            'image',
            'alt',
        ]

    fields = \
        [
            'image',
            'image_md',
            'image_xl',
            'alt',
        ]

    readonly_fields = \
        [
            'image_md',
            'image_xl',
        ]
