from flask import render_template, request

from .. import assets, preprocessors, responses
from ...util import wikimedia
from ..util import (build_maintenance_notice, build_script_tags,
                    build_style_tags)


def configure(bp, config, db):
    @bp.route("/stats/")
    def stats():
        wikis = db.campaigns.wikis()
        return render_template(
            "stats.html", wikis=sorted(list(wikis)),
            maintenance_notice=build_maintenance_notice(request, config))

    @bp.route("/stats/<wiki>/")
    def stats_wiki(wiki):
        script_tags = build_script_tags(assets.LIB_JS, config)
        style_tags = build_style_tags(assets.LIB_CSS, config)
        return render_template(
            "stats_wiki.html",
            wiki=wiki,
            script_tags=script_tags,
            style_tags=style_tags,
            campaigns=db.campaigns.for_wiki(wiki, True),
            maintenance_notice=build_maintenance_notice(request, config))

    @bp.route("/stats/<wiki>/<int:id>")
    def stats_wiki_campaign(wiki, id):
        script_tags = build_script_tags(assets.LIB_JS, config)
        style_tags = build_style_tags(assets.LIB_CSS, config)
        campaigns = db.campaigns.for_wiki(wiki, True)
        for campaign in campaigns:
            if campaign['id'] == id:
                break
        else:
            return responses.not_found()
        return render_template(
            "stats_wiki_campaign.html",
            wiki=wiki,
            script_tags=script_tags,
            style_tags=style_tags,
            campaign=campaign,
            maintenance_notice=build_maintenance_notice(request, config))

    return bp