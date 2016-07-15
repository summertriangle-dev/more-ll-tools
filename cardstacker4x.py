#!/usr/bin/env python3
# cardstacker4x: Generate SIF 4.x card images from cache.

# The Holy Constituency of the Summer Triangle, 2016.
# No rights reserved; see readme for more information.
import sys
import os
import sqlite3
from PIL import Image
from collections import namedtuple

try:
    from libcard import SMILE,PURE,COOL,ASSIST,N,R,SR,SSR,UR
except ImportError:
    # attribute
    SMILE    = 1
    PURE     = 2
    COOL     = 3
    ASSIST   = 5

    # rarity
    N   = 1
    R   = 2
    SR  = 3
    UR  = 4
    SSR = 5

layer_t = namedtuple("layer_t", ("src", "offset", "scale", "use_cache"))
def Q_LAYER(src):
    return layer_t(src, (0, 0), 1.0, 1)

HAVE_FANCY_BACKGROUND = {SSR, UR}
BACKGROUND_NAMES = {
    SMILE: {
        N: Q_LAYER("assets/image/cards/background/b_smile_N_001.png"),
        R: Q_LAYER("assets/image/cards/background/b_smile_R_001.png"),
        SR: Q_LAYER("assets/image/cards/background/b_smile_SR_001.png")
    },
    PURE: {
        N: Q_LAYER("assets/image/cards/background/b_pure_N_001.png"),
        R: Q_LAYER("assets/image/cards/background/b_pure_R_001.png"),
        SR: Q_LAYER("assets/image/cards/background/b_pure_SR_001.png")
    },
    COOL: {
        N: Q_LAYER("assets/image/cards/background/b_cool_N_001.png"),
        R: Q_LAYER("assets/image/cards/background/b_cool_R_001.png"),
        SR: Q_LAYER("assets/image/cards/background/b_cool_SR_001.png")
    },
    ASSIST: {
        N: Q_LAYER("assets/image/cards/background/b_all_N_001.png"),
        R: Q_LAYER("assets/image/cards/background/b_all_R_001.png"),
        SR: Q_LAYER("assets/image/cards/background/b_all_SR_001.png")
    }
}
BACKGROUND_NAMES_T = {
    SMILE: {
        N: Q_LAYER("assets/image/cards/background/b_smile_N_002.png"),
        R: Q_LAYER("assets/image/cards/background/b_smile_R_002.png"),
        SR: Q_LAYER("assets/image/cards/background/b_smile_SR_002.png")
    },
    PURE: {
        N: Q_LAYER("assets/image/cards/background/b_pure_N_002.png"),
        R: Q_LAYER("assets/image/cards/background/b_pure_R_002.png"),
        SR: Q_LAYER("assets/image/cards/background/b_pure_SR_002.png")
    },
    COOL: {
        N: Q_LAYER("assets/image/cards/background/b_cool_N_002.png"),
        R: Q_LAYER("assets/image/cards/background/b_cool_R_002.png"),
        SR: Q_LAYER("assets/image/cards/background/b_cool_SR_002.png")
    },
    ASSIST: {
        N: Q_LAYER("assets/image/cards/background/b_all_N_001.png"),
        R: Q_LAYER("assets/image/cards/background/b_all_R_001.png"),
        SR: Q_LAYER("assets/image/cards/background/b_all_SR_001.png")
    }
}

RARITY_NAMES = {
  SMILE: {
    N: Q_LAYER("assets/image/cards/rarity/r_smile_N.png"),
    R: Q_LAYER("assets/image/cards/rarity/r_smile_R.png"),
    SR: Q_LAYER("assets/image/cards/rarity/r_smile_SR.png"),
    SSR: Q_LAYER("assets/image/cards/rarity/r_smile_SSR.png"),
    UR: Q_LAYER("assets/image/cards/rarity/r_smile_UR.png")
  },
  PURE: {
    N: Q_LAYER("assets/image/cards/rarity/r_pure_N.png"),
    R: Q_LAYER("assets/image/cards/rarity/r_pure_R.png"),
    SR: Q_LAYER("assets/image/cards/rarity/r_pure_SR.png"),
    SSR: Q_LAYER("assets/image/cards/rarity/r_pure_SSR.png"),
    UR: Q_LAYER("assets/image/cards/rarity/r_pure_UR.png")
  },
  COOL: {
    N: Q_LAYER("assets/image/cards/rarity/r_cool_N.png"),
    R: Q_LAYER("assets/image/cards/rarity/r_cool_R.png"),
    SR: Q_LAYER("assets/image/cards/rarity/r_cool_SR.png"),
    SSR: Q_LAYER("assets/image/cards/rarity/r_cool_SSR.png"),
    UR: Q_LAYER("assets/image/cards/rarity/r_cool_UR.png")
  },
  ASSIST: {
    N: Q_LAYER("assets/image/cards/rarity/r_all_N.png"),
    R: Q_LAYER("assets/image/cards/rarity/r_all_R.png"),
    SR: Q_LAYER("assets/image/cards/rarity/r_all_SR.png"),
    SSR: Q_LAYER("assets/image/cards/rarity/r_all_SSR.png"),
    UR: Q_LAYER("assets/image/cards/rarity/r_all_UR.png")
  }
}

STAR_NAMES = {
    N: Q_LAYER("assets/image/cards/star/s_001.png"),
    R: Q_LAYER("assets/image/cards/star/s_003.png"),
    SR: Q_LAYER("assets/image/cards/star/s_005.png"),
    SSR: Q_LAYER("assets/image/cards/star/s_007.png"),
    UR: Q_LAYER("assets/image/cards/star/s_009.png")
}
STAR_NAMES_T = {
    N: Q_LAYER("assets/image/cards/star/s_002.png"),
    R: Q_LAYER("assets/image/cards/star/s_004.png"),
    SR: Q_LAYER("assets/image/cards/star/s_006.png"),
    SSR: Q_LAYER("assets/image/cards/star/s_008.png"),
    UR: Q_LAYER("assets/image/cards/star/s_010.png")
}

FRAME_NAMES = {
  SMILE: {
    N: Q_LAYER("assets/image/cards/frame/f_N_1.png"),
    R: Q_LAYER("assets/image/cards/frame/f_R_1.png"),
    SR: Q_LAYER("assets/image/cards/frame/f_SR_4.png"),
    SSR: Q_LAYER("assets/image/cards/frame/f_SSR_4.png"),
    UR: Q_LAYER("assets/image/cards/frame/f_UR_4.png")
  },
  PURE: {
    N: Q_LAYER("assets/image/cards/frame/f_N_2.png"),
    R: Q_LAYER("assets/image/cards/frame/f_R_2.png"),
    SR: Q_LAYER("assets/image/cards/frame/f_SR_4.png"),
    SSR: Q_LAYER("assets/image/cards/frame/f_SSR_4.png"),
    UR: Q_LAYER("assets/image/cards/frame/f_UR_4.png")
  },
  COOL: {
    N: Q_LAYER("assets/image/cards/frame/f_N_3.png"),
    R: Q_LAYER("assets/image/cards/frame/f_R_3.png"),
    SR: Q_LAYER("assets/image/cards/frame/f_SR_4.png"),
    SSR: Q_LAYER("assets/image/cards/frame/f_SSR_4.png"),
    UR: Q_LAYER("assets/image/cards/frame/f_UR_4.png")
  },
  ASSIST: {
    N: Q_LAYER("assets/image/cards/frame/f_N_9.png"),
    R: Q_LAYER("assets/image/cards/frame/f_R_9.png"),
    SR: Q_LAYER("assets/image/cards/frame/f_SR_4.png"),
    SSR: Q_LAYER("assets/image/cards/frame/f_SSR_4.png"),
    UR: Q_LAYER("assets/image/cards/frame/f_UR_4.png")
  }
}

BADGE_T = Q_LAYER("assets/image/cards/evolution/ev_01.png")

class CardStacker(object):
    def __init__(self, cache):
        self.cache = cache
        self.image_cache = {}
        self.unitdb = sqlite3.connect(os.path.join(cache, "db", "unit", "unit.db_"))
        self.unitdb.row_factory = sqlite3.Row
        self.carddb = sqlite3.connect(os.path.join(cache, "db", "unit", "card.db_"))
        self.carddb.row_factory = sqlite3.Row

    def unit_params(self, ordinal, rankup):
        NORMAL_Q = """SELECT unit_type_m.name_image_asset AS name_image,
                             rarity,
                             attribute_id,
                             unit_navi_asset_m.unit_navi_asset AS navi,
                             normal_card_id AS the_card
                      FROM unit_m
                      LEFT JOIN unit_navi_asset_m ON (normal_unit_navi_asset_id = unit_navi_asset_id)
                      LEFT JOIN unit_type_m USING (unit_type_id)
                      WHERE unit_number=?"""
        RANKUP_Q = """SELECT unit_type_m.name_image_asset AS name_image,
                             rarity,
                             attribute_id,
                             unit_navi_asset_m.unit_navi_asset AS navi,
                             rank_max_card_id AS the_card
                      FROM unit_m
                      LEFT JOIN unit_navi_asset_m ON (rank_max_unit_navi_asset_id = unit_navi_asset_id)
                      LEFT JOIN unit_type_m USING (unit_type_id)
                      WHERE unit_number=?"""
        cur = self.unitdb.execute(RANKUP_Q if (rankup & 1) else NORMAL_Q, (ordinal,))
        return cur.fetchone()

    def card_params(self, id):
        cur = self.carddb.execute("SELECT navi_move_x, navi_move_y, navi_size_ratio, flash_asset FROM card_m WHERE card_id=?", (id,))
        return cur.fetchone()

    def get_every_card(self):
        cur = self.unitdb.execute("SELECT DISTINCT unit_number FROM unit_m")
        return [x for x, in cur.fetchall()]

    def valid_formes_for_unit(self, ordinal):
        cur = self.unitdb.execute("SELECT (normal_icon_asset == rank_max_icon_asset) AS is_pretransformed, disable_rank_up, rarity FROM unit_m WHERE unit_number=?", (ordinal,))
        is_pt, is_td, rarity = cur.fetchone()

        if is_td:
            bse = [0]
        elif is_pt:
            bse = [1]
        else:
            bse = [0, 1]

        if rarity in HAVE_FANCY_BACKGROUND:
            if 0 in bse: # clean normal
                bse.append(2)
            if 1 in bse: # clean t
                bse.append(3)

        return bse

    def layer_order_for_unit(self, ordinal, rankup):
        order = []

        unit = self.unit_params(ordinal, rankup)
        card = self.card_params(unit["the_card"])

        if rankup:
            l_BACKGROUND_NAMES = BACKGROUND_NAMES_T
            l_STAR_NAMES = STAR_NAMES_T
        else:
            l_BACKGROUND_NAMES = BACKGROUND_NAMES
            l_STAR_NAMES = STAR_NAMES

        if unit["rarity"] in HAVE_FANCY_BACKGROUND:
            order.append(layer_t(card["flash_asset"], (0, 0), 1.0, 0))

            if rankup > 1:
                return order
        else:
            order.append(l_BACKGROUND_NAMES[unit["attribute_id"]][unit["rarity"]])
            order.append(layer_t(unit["navi"], (card["navi_move_x"], card["navi_move_y"]), card["navi_size_ratio"], 0))

        order.append(FRAME_NAMES[unit["attribute_id"]][unit["rarity"]])
        order.append(layer_t(unit["name_image"], (0, 0), 1.0, 0))
        order.append(l_STAR_NAMES[unit["rarity"]])
        order.append(RARITY_NAMES[unit["attribute_id"]][unit["rarity"]])

        if rankup:
            order.append(BADGE_T)

        return order

    def get_layer_image(self, layer):
        if layer.src not in self.image_cache:
            i = Image.open(os.path.join(self.cache, layer.src))
            i = i.convert("RGBA")
            if layer.scale != 1.0:
                i = i.resize((round(i.size[0] * layer.scale), round(i.size[1] * layer.scale)), Image.BILINEAR)

            if layer.use_cache:
                self.image_cache[layer.src] = i
            ret = i
        else:
            ret = self.image_cache[layer.src]
        return ret

    def composite(self, order):
        canvas = Image.new("RGBA", (512, 720))
        for layer in order:
            print("...", layer)
            im = self.get_layer_image(layer)
            canvas.paste(im, layer.offset, im)
        return canvas

SUFFIX_FOR_FORME = {
    0: "",
    1: "_t",
    2: "_c",
    3: "_ct"
}
def main(cache: "SIF Application Support dump",
         output,
        *cards: "list of card ordinals"):
    cache = CardStacker(cache)

    if not cards:
        cards = cache.get_every_card()

    for card in cards:
        states = cache.valid_formes_for_unit(int(card))
        for t in states:
            name = "card_{0}{1}.png".format(card, SUFFIX_FOR_FORME.get(t, ""))
            fullpath = os.path.join(output, name)
            if os.path.exists(fullpath):
                print("not touching", name, "because it already exists")
                continue

            order = cache.layer_order_for_unit(int(card), t)
            print(name)
            cache.composite(order).save(fullpath)

if __name__ == '__main__':
    import plac
    plac.call(main)
