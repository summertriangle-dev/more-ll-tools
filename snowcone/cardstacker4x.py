#!/usr/bin/env python3
# This is a modified version of cs4x!! It will not produce
# the same result as the standalone version in this repo

import sys
import os
import sqlite3
from PIL import Image
from collections import namedtuple

SMILE    = 1
PURE     = 2
COOL     = 3
ASSIST   = 5

N   = 1
R   = 2
SR  = 3
UR  = 4
SSR = 5

stack_t = namedtuple("stack_t", ("size", "order"))
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

ICON_BG_NAMES = {
    SMILE: Q_LAYER("assets/image/ui/common/com_win_19.png"),
    PURE: Q_LAYER("assets/image/ui/common/com_win_20.png"),
    COOL: Q_LAYER("assets/image/ui/common/com_win_18.png"),
    ASSIST: Q_LAYER("assets/image/ui/common/com_win_21.png"),
}
ICON_BG_NAME_T = Q_LAYER("assets/image/ui/common/com_win_55.png")

BACKING_NAMES = {
  SMILE: {
    N: Q_LAYER("assets/image/cards/icon/b_smile_N_001.png"),
    R: Q_LAYER("assets/image/cards/icon/b_smile_R_001.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_smile_SR_001.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  },
  PURE: {
    N: Q_LAYER("assets/image/cards/icon/b_pure_N_001.png"),
    R: Q_LAYER("assets/image/cards/icon/b_pure_R_001.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_pure_SR_001.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  },
  COOL: {
    N: Q_LAYER("assets/image/cards/icon/b_cool_N_001.png"),
    R: Q_LAYER("assets/image/cards/icon/b_cool_R_001.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_cool_SR_001.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  },
  ASSIST: {
    N: Q_LAYER("assets/image/cards/icon/b_all_N_001.png"),
    R: Q_LAYER("assets/image/cards/icon/b_all_R_001.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_all_SR_001.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  }
}

BACKING_NAMES_T = {
  SMILE: {
    N: Q_LAYER("assets/image/cards/icon/b_smile_N_002.png"),
    R: Q_LAYER("assets/image/cards/icon/b_smile_R_002.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_smile_SR_002.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  },
  PURE: {
    N: Q_LAYER("assets/image/cards/icon/b_pure_N_002.png"),
    R: Q_LAYER("assets/image/cards/icon/b_pure_R_002.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_pure_SR_002.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  },
  COOL: {
    N: Q_LAYER("assets/image/cards/icon/b_cool_N_002.png"),
    R: Q_LAYER("assets/image/cards/icon/b_cool_R_002.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_cool_SR_002.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  },
  ASSIST: {
    N: Q_LAYER("assets/image/cards/icon/b_all_N_002.png"),
    R: Q_LAYER("assets/image/cards/icon/b_all_R_002.png"),
    SR: Q_LAYER("assets/image/cards/icon/b_all_SR_002.png"),
    SSR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
    UR: Q_LAYER("assets/image/cards/icon/b_all_SSR_001.png"),
  }
}

RING_NAMES = {
  SMILE: {
    N: Q_LAYER("assets/image/cards/icon/f_N_1.png"),
    R: Q_LAYER("assets/image/cards/icon/f_R_1.png"),
    SR: Q_LAYER("assets/image/cards/icon/f_SR_1.png"),
    SSR: Q_LAYER("assets/image/cards/icon/f_SSR_1.png"),
    UR: Q_LAYER("assets/image/cards/icon/f_UR_1.png"),
  },
  PURE: {
    N: Q_LAYER("assets/image/cards/icon/f_N_2.png"),
    R: Q_LAYER("assets/image/cards/icon/f_R_2.png"),
    SR: Q_LAYER("assets/image/cards/icon/f_SR_2.png"),
    SSR: Q_LAYER("assets/image/cards/icon/f_SSR_2.png"),
    UR: Q_LAYER("assets/image/cards/icon/f_UR_2.png"),
  },
  COOL: {
    N: Q_LAYER("assets/image/cards/icon/f_N_3.png"),
    R: Q_LAYER("assets/image/cards/icon/f_R_3.png"),
    SR: Q_LAYER("assets/image/cards/icon/f_SR_3.png"),
    SSR: Q_LAYER("assets/image/cards/icon/f_SSR_3.png"),
    UR: Q_LAYER("assets/image/cards/icon/f_UR_3.png"),
  },
  ASSIST: {
    N: Q_LAYER("assets/image/cards/icon/f_N_9.png"),
    R: Q_LAYER("assets/image/cards/icon/f_R_9.png"),
    SR: Q_LAYER("assets/image/cards/icon/f_SR_9.png"),
    SSR: Q_LAYER("assets/image/cards/icon/f_SSR_9.png"),
    UR: Q_LAYER("assets/image/cards/icon/f_UR_9.png"),
  }
}

BADGE_NAMES = {
  SMILE: {
    N: Q_LAYER("assets/image/ui/common/com_icon_05.png"),
    R: Q_LAYER("assets/image/ui/common/com_icon_06.png"),
    SR: Q_LAYER("assets/image/ui/common/com_icon_07.png"),
    SSR: Q_LAYER("assets/image/ui/common/com_icon_08.png"),
    UR: Q_LAYER("assets/image/ui/common/com_icon_09.png"),
  },
  PURE: {
    N: Q_LAYER("assets/image/ui/common/com_icon_10.png"),
    R: Q_LAYER("assets/image/ui/common/com_icon_11.png"),
    SR: Q_LAYER("assets/image/ui/common/com_icon_12.png"),
    SSR: Q_LAYER("assets/image/ui/common/com_icon_54.png"),
    UR: Q_LAYER("assets/image/ui/common/com_icon_55.png"),
  },
  COOL: {
    N: Q_LAYER("assets/image/ui/common/com_icon_56.png"),
    R: Q_LAYER("assets/image/ui/common/com_icon_57.png"),
    SR: Q_LAYER("assets/image/ui/common/com_icon_58.png"),
    SSR: Q_LAYER("assets/image/ui/common/com_icon_59.png"),
    UR: Q_LAYER("assets/image/ui/common/com_icon_60.png"),
  },
  ASSIST: {
    N: Q_LAYER("assets/image/ui/common/com_icon_61.png"),
    R: Q_LAYER("assets/image/ui/common/com_icon_62.png"),
    SR: Q_LAYER("assets/image/ui/common/com_icon_63.png"),
    SSR: Q_LAYER("assets/image/ui/common/com_icon_64.png"),
    UR: Q_LAYER("assets/image/ui/common/com_icon_65.png"),
  }
}

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
                             normal_icon_asset AS icon,
                             normal_card_id AS the_card,
                             disable_rank_up
                      FROM unit_m
                      LEFT JOIN unit_navi_asset_m ON (normal_unit_navi_asset_id = unit_navi_asset_id)
                      LEFT JOIN unit_type_m USING (unit_type_id)
                      WHERE unit_number=?"""
        RANKUP_Q = """SELECT unit_type_m.name_image_asset AS name_image,
                             rarity,
                             attribute_id,
                             unit_navi_asset_m.unit_navi_asset AS navi,
                             rank_max_icon_asset AS icon,
                             rank_max_card_id AS the_card,
                             disable_rank_up
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
            # bse = [0, 4, 8]
            # FIXME: dirty hack for schoolidolu, where is_transform_disabled == pre-transformed for some reason.
            bse = [1, 5, 9]
        elif is_pt:
            bse = [1, 5, 9]
        else:
            bse = [0, 1, 4, 5, 8, 9]

        if rarity in HAVE_FANCY_BACKGROUND:
            if 0 in bse: # clean normal
                bse.append(2)
            if 1 in bse: # clean t
                bse.append(3)

        return bse

    def layer_order_for_unit(self, ordinal, forme):
        order = []

        unit = self.unit_params(ordinal, forme)

        if unit["disable_rank_up"] and forme & 1:
            # FIXME: dirty hack for schoolidolu, where is_transform_disabled == pre-transformed for some reason.
            return self.layer_order_for_unit(ordinal, forme & 0b1111110)

        if forme & 0b1000:
            return stack_t((1024, 1024), [
                layer_t(unit["navi"], (0, 0), 1.0, 0)])
        elif forme & 0b100:
            if forme & 1:
                order.append(ICON_BG_NAME_T)
            else:
                order.append(ICON_BG_NAMES[unit["attribute_id"]])

            if unit["rarity"] not in HAVE_FANCY_BACKGROUND:
                if forme & 1:
                    order.append(BACKING_NAMES_T[unit["attribute_id"]][unit["rarity"]])
                else:
                    order.append(BACKING_NAMES[unit["attribute_id"]][unit["rarity"]])

            order.append(layer_t(unit["icon"], (0, 0), 1.0, 0))

            order.append(RING_NAMES[unit["attribute_id"]][unit["rarity"]])
            order.append(BADGE_NAMES[unit["attribute_id"]][unit["rarity"]])

            return stack_t((128, 128), order)
        else:
            card = self.card_params(unit["the_card"])

            if forme & 1:
                l_BACKGROUND_NAMES = BACKGROUND_NAMES_T
                l_STAR_NAMES = STAR_NAMES_T
            else:
                l_BACKGROUND_NAMES = BACKGROUND_NAMES
                l_STAR_NAMES = STAR_NAMES

            if unit["rarity"] in HAVE_FANCY_BACKGROUND:
                order.append(layer_t(card["flash_asset"], (0, 0), 1.0, 0))

                if forme & 0b10:
                    return stack_t((512, 720), order)
            else:
                order.append(l_BACKGROUND_NAMES[unit["attribute_id"]][unit["rarity"]])
                order.append(layer_t(unit["navi"], (card["navi_move_x"], card["navi_move_y"]), card["navi_size_ratio"], 0))

            order.append(FRAME_NAMES[unit["attribute_id"]][unit["rarity"]])
            order.append(layer_t(unit["name_image"], (0, 0), 1.0, 0))
            order.append(l_STAR_NAMES[unit["rarity"]])
            order.append(RARITY_NAMES[unit["attribute_id"]][unit["rarity"]])

            if forme & 1:
                pass
                # order.append(BADGE_T)

            return stack_t((512, 720), order)

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

    def composite(self, stack):
        canvas = Image.new("RGBA", stack.size)
        for layer in stack.order:
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
def main(cache, output, *cards):
    cache = CardStacker(cache)

    if not cards:
        cards = cache.get_every_card()

    for card in cards:
        try:
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
        except:
            continue

if __name__ == '__main__':
    import plac
    plac.call(main)
