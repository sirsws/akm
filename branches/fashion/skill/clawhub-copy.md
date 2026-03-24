<!--
文件：clawhub-copy.md
核心功能：作为 Fashion skill 的正式发布页文案，供 ClawHub / OpenClaw 或同类技能市场直接复用。
输入：Fashion 分支的 AKM 定位、方法结构、外部测试结论与使用边界。
输出：可直接上线的技能页长版文案。
-->

# AKM Fashion ClawHub Skill Page

## Skill Title

**AKM Fashion: Context-Aware Wardrobe Strategist**

## One-line Description

Model the user's body, scenes, wardrobe, and constraints first, then make outfit and purchase decisions that actually fit.

## What It Is

Most styling agents answer too early.

They do not know what the user owns, what scenes matter, what body issues need handling, or what functional constraints exist.
That is where generic style advice starts.

AKM Fashion fixes this by building a usable fashion profile first:

- body context
- primary scenes
- style preferences
- wardrobe assets
- functional constraints
- anti-patterns

Only then does it produce outfit and wardrobe decisions.

## What Makes It Different

This is not a stylist persona prompt.
It is a three-stage method:

1. elicitation
2. structured record
3. execution decision

The output is not a moodboard.
It is a wardrobe-aware judgment.

## Best Fit

Use this skill when:

- the user needs scene-specific outfit decisions
- current wardrobe materially constrains the solution space
- comfort and function matter, not only aesthetics
- the user wants purchase priorities, not vague taste talk

## Boundary

- not an image recognition tool
- not a virtual try-on product
- does not pretend unknown wardrobe assets are known
- does not replace scene judgment with vague style labels

## Closing Line

**No wardrobe model, no serious styling advice.**